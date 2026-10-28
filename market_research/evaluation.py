"""Reproducible SYNTHETIC stress suite with labels independent of the detector.

The task is triage of injected regime changes, not prediction of settlement.
These labels and generators are hand-designed; a separate RNG seed is not
independent real-market evidence. Keep failure cases and do not tune on holdout.
"""

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import random

from .agents import judge
from .analysis import Config, analyze
from .audit import atomic_text, canonical_json, code_digest, digest, write_json
from .models import Market

ACTIONS = ("investigate", "monitor", "abstain")
FAMILIES = {
    "quiet_market": "monitor",
    "large_injected_jump": "investigate",
    "small_injected_jump": "investigate",
    "ordinary_high_volatility": "monitor",
    "injected_activity_surge": "investigate",
    "wide_spread_with_jump": "abstain",
    "missing_quotes_with_jump": "abstain",
    "stale_capture_with_jump": "abstain",
    "insufficient_history": "monitor",
    "changed_resolution_rules": "monitor",
    "ordinary_gradual_drift": "monitor",
    "expired_close_with_jump": "abstain",
}


@dataclass
class Case:
    case_id: str
    split: str
    family: str
    expected: str
    as_of: str
    market: Market
    history: list[Market]

    def to_dict(self):
        return {
            "case_id": self.case_id,
            "split": self.split,
            "family": self.family,
            "expected": self.expected,
            "as_of": self.as_of,
            "market": self.market.to_dict(),
            "history": [
                {
                    key: getattr(m, key)
                    for key in (
                        "observed_at",
                        "probability",
                        "probability_basis",
                        "rules",
                        "volume_24h",
                    )
                }
                for m in self.history
            ],
        }


def generate_cases(seed: int, count: int) -> list[Case]:
    if not 1 <= count <= 100:
        raise ValueError("cases-per-family must be between 1 and 100")
    result = []
    epoch = datetime(2026, 10, 28, 8, tzinfo=timezone.utc)
    for split, offset in [("calibration", 0), ("holdout", 104729)]:
        rng = random.Random(seed + offset)
        for family, expected in FAMILIES.items():
            for index in range(count):
                source = "polymarket" if index % 2 == 0 else "kalshi"
                case_id = f"{split}/{family}/{index:03d}"
                current_time = epoch - timedelta(
                    hours=2 if family == "stale_capture_with_jump" else 0
                )
                unit = "usd" if source == "polymarket" else "contracts"
                volume = rng.uniform(20000, 60000) if unit == "usd" else rng.uniform(1000, 8000)
                initial = rng.uniform(0.35, 0.60)
                history = []
                current_p = initial
                for hour in range(49):
                    # Normal observation noise is distinct from injected regime shifts.
                    sigma = 0.026 if family == "ordinary_high_volatility" else 0.0015
                    if family == "ordinary_gradual_drift":
                        current_p = initial + hour * 0.0016 + rng.gauss(0, 0.0008)
                    else:
                        current_p += rng.gauss(0, sigma)
                    current_p = min(0.88, max(0.12, current_p))
                    if hour == 48 and (
                        family.endswith("with_jump") or family == "large_injected_jump"
                    ):
                        current_p = min(0.94, current_p + rng.uniform(0.065, 0.11))
                    elif hour == 48 and family == "small_injected_jump":
                        current_p += rng.uniform(0.025, 0.040)
                    observed_at = (current_time - timedelta(hours=48 - hour)).isoformat()
                    m = Market(
                        source,
                        case_id,
                        "[SYNTHETIC EVALUATION] " + family,
                        observed_at,
                        observed_at,
                        "2026-12-31T23:59:00Z",
                        True,
                        current_p,
                        "outcome_price_yes" if unit == "usd" else "yes_midpoint",
                        max(current_p - 0.01, 0),
                        min(current_p + 0.01, 1),
                        volume,
                        1_000_000 + hour * 1000,
                        unit,
                        20000 if unit == "usd" else None,
                        "Synthetic settlement rule A. No real event.",
                        "",
                    )
                    history.append(m)
                current = history[-1]
                if family == "injected_activity_surge":
                    current.volume_24h *= rng.uniform(3.5, 6)
                elif family == "wide_spread_with_jump":
                    current.yes_bid, current.yes_ask = current_p - 0.12, current_p + 0.12
                elif family == "missing_quotes_with_jump":
                    current.yes_bid = current.yes_ask = None
                elif family == "expired_close_with_jump":
                    current.close_time = (current_time - timedelta(days=1)).isoformat()
                elif family == "changed_resolution_rules":
                    current.rules = "Synthetic settlement rule B; distinct contract semantics."
                if family == "insufficient_history":
                    history = [current]
                result.append(
                    Case(case_id, split, family, expected, epoch.isoformat(), current, history)
                )
    return result


def classification_metrics(rows: list[dict]) -> dict:
    confusion = {a: {b: 0 for b in ACTIONS} for a in ACTIONS}
    for row in rows:
        confusion[row["expected"]][row["predicted"]] += 1
    per_class = {}
    for action in ACTIONS:
        tp = confusion[action][action]
        support = sum(confusion[action].values())
        predicted = sum(confusion[expected][action] for expected in ACTIONS)
        precision = tp / predicted if predicted else 0
        recall = tp / support if support else 0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
        per_class[action] = {
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1": round(f1, 4),
            "support": support,
        }
    unsafe = sum(row["expected"] == "abstain" and row["predicted"] != "abstain" for row in rows)
    return {
        "cases": len(rows),
        "confusion_matrix": confusion,
        "per_class": per_class,
        "accuracy": round(sum(confusion[a][a] for a in ACTIONS) / len(rows), 4) if rows else 0,
        "macro_f1": round(sum(per_class[a]["f1"] for a in ACTIONS) / len(ACTIONS), 4),
        "unsafe_non_abstentions": unsafe,
        "false_research_alerts": sum(
            row["expected"] == "monitor" and row["predicted"] == "investigate" for row in rows
        ),
    }


def evaluate(out: Path, seed: int, count: int, cfg: Config) -> dict:
    cases = generate_cases(seed, count)
    dataset = [c.to_dict() for c in cases]
    atomic_text(out / "dataset.jsonl", "".join(canonical_json(c) + "\n" for c in dataset))
    variants = {
        "fixed_thresholds": replace(cfg, enable_robust_z=False, enable_activity_surge=False),
        "fixed_plus_robust": replace(cfg, enable_activity_surge=False),
        "full_pipeline": cfg,
        "without_risk_gates": cfg,
    }
    rows = []
    for name, config in variants.items():
        for case in cases:
            a = analyze(case.market, case.history, config, case.as_of)
            if name == "without_risk_gates":
                a = replace(a, eligible=True, exclusion_reasons=[])
            decision = judge(a).decision
            rows.append(
                {
                    "variant": name,
                    "split": case.split,
                    "case_id": case.case_id,
                    "family": case.family,
                    "expected": case.expected,
                    "predicted": decision["action"],
                    "blocks": a.exclusion_reasons,
                    "signals": [s.kind for s in a.signals],
                    "features": {
                        key: value
                        for key, value in a.evidence.items()
                        if key
                        in {
                            "e_change_1h",
                            "e_change_24h",
                            "e_robust_z",
                            "e_volume_ratio",
                            "e_spread",
                        }
                    },
                }
            )
    results = {}
    for split in ("calibration", "holdout"):
        results[split] = {
            name: classification_metrics(
                [r for r in rows if r["split"] == split and r["variant"] == name]
            )
            for name in variants
        }
    report = {
        "schema_version": "1.0",
        "data_mode": "synthetic_stress_evaluation",
        "seed": seed,
        "holdout_seed_offset": 104729,
        "cases_per_family_per_split": count,
        "families": FAMILIES,
        "dataset_sha256": digest(dataset),
        "code_sha256": code_digest(),
        "config": cfg.to_dict(),
        "results": results,
        "limitations": [
            "Hand-designed synthetic generators and labels, not independent market annotations.",
            "A held-out RNG seed tests robustness within generators, not out-of-distribution generalization.",
            "No parameters were tuned by this evaluation command; inspect failures, not just averages.",
            "No LLM, real-market detection accuracy, settlement accuracy or returns are measured.",
            "The no-risk variant deliberately bypasses gates only inside this experiment.",
        ],
        "predictions": rows,
    }
    write_json(out / "evaluation.json", report)
    lines = [
        "# Synthetic stress evaluation",
        "",
        "**Not real-market accuracy. No LLM was called.**",
        "",
        f"Seed: {seed}; holdout seed: {seed + 104729}; dataset SHA-256: `{digest(dataset)}`.",
        f"Total labeled cases: {len(cases)}; {len(FAMILIES)} families; "
        f"{count} cases/family/split; {len(rows)} variant decisions.",
        "",
        "Labels follow injected regime-change and data-quality scenarios, independently of detector output.",
        "The same family generators are shared across splits; this is not real-world external validation.",
        "",
    ]
    for split in results:
        lines.extend(
            [
                f"## {split}",
                "",
                "| Variant | Macro F1 | Alert precision | Alert recall | Unsafe non-abstain | False alerts |",
                "|---|---:|---:|---:|---:|---:|",
            ]
        )
        for name, result in results[split].items():
            alert = result["per_class"]["investigate"]
            lines.append(
                f"| {name} | {result['macro_f1']:.3f} | {alert['precision']:.3f} | "
                f"{alert['recall']:.3f} | {result['unsafe_non_abstentions']} | "
                f"{result['false_research_alerts']} |"
            )
        lines.append("")
    lines.extend(
        [
            "## Failure cases from the full pipeline",
            "",
            "Every error is retained in evaluation.json. First 20 holdout failures:",
            "",
            "| Case | Expected | Actual | Signals |",
            "|---|---|---|---|",
        ]
    )
    failures = [
        r
        for r in rows
        if r["variant"] == "full_pipeline"
        and r["split"] == "holdout"
        and r["expected"] != r["predicted"]
    ]
    for row in failures[:20]:
        lines.append(
            f"| {row['case_id']} | {row['expected']} | {row['predicted']} | "
            f"{', '.join(row['signals']) or 'none'} |"
        )
    lines.extend(
        [
            "",
            "## Interpretation and next experiment",
            "",
            "Fixed thresholds can miss small shifts in quiet markets; a robust relative detector can "
            "recover some of them. Ordinary high-volatility paths can also cross the fixed 24h "
            "threshold, so higher recall may come with extra review alerts. The labels deliberately "
            "distinguish injected shifts from ordinary variation; inspect that mismatch before tuning.",
            "",
            "Risk-gate ablation shows what happens when invalid inputs are allowed through. "
            "Neither this result nor a high synthetic F1 establishes financial value.",
            "",
            "Next: annotate a fixed real watchlist for feed gaps, ordinary repricing and unusual "
            "repricing, freeze a time-based held-out period, and compare with the same metrics.",
            "",
            "## Limits",
            "",
        ]
        + ["- " + s for s in report["limitations"]]
    )
    atomic_text(out / "evaluation.md", "\n".join(lines) + "\n")
    return {
        "data_mode": report["data_mode"],
        "cases": len(cases),
        "variants": len(variants),
        "holdout": results["holdout"],
        "report": str((out / "evaluation.md").resolve()),
    }
