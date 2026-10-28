"""Explainable research-priority ranking, time-matched deltas and anomaly rules."""

from dataclasses import asdict, dataclass
import math
import statistics

from .models import Analysis, Market, Signal, parse_time
from .native_history import NativeHistory, features as native_features


@dataclass(frozen=True)
class Config:
    min_polymarket_volume: float = 1000  # USD in rolling 24h
    min_kalshi_volume: float = 100  # contracts in rolling 24h
    max_spread: float = 0.08
    min_probability: float = 0.02
    max_probability: float = 0.98
    jump_1h: float = 0.05
    jump_24h: float = 0.10
    rolling_volume_ratio: float = 3.0
    robust_z: float = 4.0
    max_snapshot_age_minutes: float = 30
    enable_fixed_jumps: bool = True
    enable_robust_z: bool = True
    enable_activity_surge: bool = True

    def __post_init__(self):
        for key, value in self.to_dict().items():
            if key.startswith("enable_"):
                if not isinstance(value, bool):
                    raise ValueError(f"{key} must be a boolean")
            elif (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
            ):
                raise ValueError(f"{key} must be a finite nonnegative number")
        if not 0 <= self.min_probability < self.max_probability <= 1:
            raise ValueError("Invalid probability selection interval")
        if self.max_spread > 1 or self.max_snapshot_age_minutes == 0:
            raise ValueError("Invalid spread/freshness configuration")

    def to_dict(self):
        return asdict(self)


def _same_contract(a: Market, b: Market) -> bool:
    return (
        a.key == b.key
        and a.probability_basis == b.probability_basis
        and a.rules == b.rules
        and a.volume_unit == b.volume_unit
    )


def _baseline(current: Market, history: list[Market], hours: float) -> Market | None:
    now = parse_time(current.observed_at)
    tolerance = 0.25 if hours == 1 else 2.0
    candidates = [
        m
        for m in history
        if _same_contract(current, m)
        and m.probability is not None
        and abs((now - parse_time(m.observed_at)).total_seconds() / 3600 - hours) <= tolerance
    ]
    return (
        min(
            candidates,
            key=lambda m: abs((now - parse_time(m.observed_at)).total_seconds() / 3600 - hours),
        )
        if candidates
        else None
    )


def analyze(
    m: Market, history: list[Market], cfg: Config, as_of: str, native: NativeHistory | None = None
) -> Analysis:
    t = parse_time(m.observed_at)
    # Filter again here so callers cannot accidentally introduce future evidence.
    history = sorted(
        [h for h in history if _same_contract(m, h) and parse_time(h.observed_at) <= t],
        key=lambda h: parse_time(h.observed_at),
    )
    history = list({h.observed_at: h for h in history + [m]}.values())
    history.sort(key=lambda h: parse_time(h.observed_at))
    e = {
        "e_probability": {
            "value": m.probability,
            "basis": m.probability_basis,
            "observed_at": m.observed_at,
        },
        "e_volume_24h": {"value": m.volume_24h, "unit": m.volume_unit, "window": "rolling_24h"},
        "e_spread": {"value": m.spread, "unit": "probability"},
        "e_rules": {"text": m.rules[:6000], "truncated": len(m.rules) > 6000},
        "e_quality": {
            "issues": m.issues,
            "snapshot_age_minutes": round((parse_time(as_of) - t).total_seconds() / 60, 3),
            "source_updated_at": m.source_updated_at,
            "note": "Source updated time is metadata time, not a quote timestamp.",
        },
    }
    reasons: list[str] = []
    signals: list[Signal] = []
    native_evidence = native_features(native, m, as_of) if native else {}
    if native_evidence:
        e["e_native_history"] = native_evidence["e_native_history"]
    if not m.active:
        reasons.append("inactive_market")
    if m.probability is None:
        reasons.append("missing_probability")
    elif not cfg.min_probability <= m.probability <= cfg.max_probability:
        reasons.append("near_resolved_probability")
    minimum = cfg.min_polymarket_volume if m.source == "polymarket" else cfg.min_kalshi_volume
    if m.volume_24h is None or m.volume_24h < minimum:
        reasons.append("insufficient_24h_activity")
    if m.spread is None:
        reasons.append("missing_two_sided_quote")
    elif m.spread > cfg.max_spread:
        reasons.append("wide_spread")
        signals.append(
            Signal(
                "wide_spread",
                "high",
                ["e_spread"],
                f"YES spread {m.spread:.1%} exceeds {cfg.max_spread:.1%}.",
            )
        )
    if not m.rules:
        reasons.append("missing_resolution_rules")
    if any(x in m.issues for x in {"invalid_or_empty_quote", "inconsistent_outcome_prices"}):
        reasons.append("invalid_market_data")
    if m.close_time:
        try:
            if parse_time(m.close_time) <= parse_time(as_of):
                reasons.append("past_scheduled_close")
        except ValueError:
            reasons.append("invalid_close_time")
    else:
        reasons.append("missing_close_time")
    exact_age_minutes = (parse_time(as_of) - t).total_seconds() / 60
    if not 0 <= exact_age_minutes <= cfg.max_snapshot_age_minutes:
        reasons.append("stale_or_future_snapshot")

    for hours, threshold in [(1, cfg.jump_1h), (24, cfg.jump_24h)]:
        previous = _baseline(m, history, hours)
        key = f"e_change_{hours}h"
        if previous and m.probability is not None:
            delta = m.probability - previous.probability
            elapsed = (t - parse_time(previous.observed_at)).total_seconds() / 3600
            e[key] = {
                "value": round(delta, 8),
                "unit": "probability",
                "elapsed_hours": round(elapsed, 4),
                "baseline_observed_at": previous.observed_at,
                "baseline_probability": previous.probability,
                "origin": "local_snapshots",
                "basis": m.probability_basis,
                "current_probability": m.probability,
                "current_event_time": m.observed_at,
            }
            if cfg.enable_fixed_jumps and abs(delta) >= threshold:
                signals.append(
                    Signal(
                        f"probability_jump_{hours}h",
                        "high",
                        [key],
                        f"YES changed {delta * 100:+.2f} pp over {elapsed:.2f}h.",
                    )
                )
        else:
            e[key] = native_evidence.get(
                key, {"value": None, "reason": "no_time_and_basis_matched_baseline"}
            )
            if (
                cfg.enable_fixed_jumps
                and e[key]["value"] is not None
                and abs(e[key]["value"]) >= threshold
            ):
                signals.append(
                    Signal(
                        f"probability_jump_{hours}h",
                        "high",
                        [key, "e_native_history"],
                        f"Native YES series changed {e[key]['value'] * 100:+.2f} pp over "
                        f"{e[key]['elapsed_hours']:.2f}h ({e[key]['basis']}).",
                    )
                )

    baseline_24h = _baseline(m, history, 24)
    if (
        baseline_24h
        and baseline_24h.volume_24h is not None
        and baseline_24h.volume_24h >= minimum
        and m.volume_24h is not None
    ):
        ratio = m.volume_24h / baseline_24h.volume_24h
        e["e_volume_ratio"] = {
            "value": round(ratio, 4),
            "unit": "ratio",
            "baseline_observed_at": baseline_24h.observed_at,
            "note": "Ratio of rolling-24h volumes, not interval traded flow.",
        }
        if cfg.enable_activity_surge and ratio >= cfg.rolling_volume_ratio:
            signals.append(
                Signal(
                    "rolling_activity_surge",
                    "medium",
                    ["e_volume_ratio"],
                    f"Rolling-24h volume is {ratio:.2f}x its day-ago level.",
                )
            )

    # Comparable cadence only: hourly moves from snapshots spaced 0.5-1.5 hours.
    # The final move is excluded from the robust baseline to avoid self-dilution.
    moves: list[tuple[Market, Market, float]] = []
    for a, b in zip(history, history[1:]):
        elapsed = (parse_time(b.observed_at) - parse_time(a.observed_at)).total_seconds() / 3600
        if 0.5 <= elapsed <= 1.5 and a.probability is not None and b.probability is not None:
            moves.append((a, b, (b.probability - a.probability) / elapsed))
    if len(moves) >= 9 and moves[-1][1].observed_at == m.observed_at:
        past = [x[2] for x in moves[:-1]]
        center = statistics.median(past)
        mad = statistics.median(abs(x - center) for x in past)
        scale = max(1.4826 * mad, 0.005)  # 0.5 pp/hour floor for flat histories
        z = (moves[-1][2] - center) / scale
        e["e_robust_z"] = {
            "value": round(z, 4),
            "baseline_moves": len(past),
            "median_rate": center,
            "mad": mad,
            "scale_floor": 0.005,
            "unit": "robust_standardized_hourly_move",
        }
        if cfg.enable_robust_z and abs(z) >= cfg.robust_z:
            signals.append(
                Signal(
                    "unusual_hourly_move",
                    "high",
                    ["e_robust_z"],
                    f"Hourly move robust z={z:.2f}; {len(past)} prior moves.",
                )
            )
    else:
        e["e_robust_z"] = native_evidence.get(
            "e_robust_z", {"value": None, "reason": "need_8_prior_comparable_hourly_moves"}
        )
        z = e["e_robust_z"]["value"]
        if cfg.enable_robust_z and z is not None and abs(z) >= cfg.robust_z:
            signals.append(
                Signal(
                    "unusual_hourly_move",
                    "high",
                    ["e_robust_z", "e_native_history"],
                    f"Native hourly move robust z={z:.2f} ({native.basis}).",
                )
            )

    # This ranks research attention, not expected return or probability of winning.
    p = m.probability
    entropy = (-p * math.log2(p) - (1 - p) * math.log2(1 - p)) if p and p < 1 else 0
    scale = 6 if m.source == "polymarket" else 5
    activity = min(math.log10((m.volume_24h or 0) + 1) / scale, 1)
    quote_quality = max(0, 1 - (m.spread if m.spread is not None else 1) / 0.15)
    events = min(sum(s.kind != "wide_spread" for s in signals) / 3, 1)
    score = round(
        100 * (0.35 * activity + 0.25 * entropy + 0.20 * quote_quality + 0.20 * events), 2
    )
    e["e_priority"] = {
        "value": score,
        "activity_component": round(activity, 4),
        "entropy_component": round(entropy, 4),
        "quote_component": round(quote_quality, 4),
        "signal_component": round(events, 4),
        "note": "Heuristic research priority; volume scales differ by venue.",
    }
    return Analysis(m, not reasons, reasons, score, e, signals)
