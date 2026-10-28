"""Commands: offline demo, live collection, and point-in-time history analysis."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
import tomllib
import platform

from . import __version__
from .adapters import collect
from .agents import judge
from .analysis import Config, analyze
from .audit import code_digest, digest, verify_manifest, write_audit
from .demo import DEMO_AS_OF, demo_snapshots
from .models import Market, parse_time, utc_now
from .native_history import NativeHistory, backfill
from .report import write_json, write_reports
from .store import Store
from .transport import JsonHTTP


def positive_int(value):
    n = int(value)
    if n < 1:
        raise argparse.ArgumentTypeError("Must be positive")
    return n


def make_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    commands = parser.add_subparsers(dest="command", required=True)
    demo = commands.add_parser("demo", help="Offline synthetic scenarios; no keys or network")
    demo.add_argument("--out", type=Path, default=Path("reports/demo"))
    replay = commands.add_parser(
        "replay", help="Offline replay of a captured live API snapshot bundle"
    )
    replay.add_argument("--bundle", type=Path, required=True)
    replay.add_argument("--out", type=Path, default=Path("reports/replay"))
    replay.add_argument("--top", type=positive_int, default=20)
    for name in ("collect", "analyze"):
        cmd = commands.add_parser(name)
        cmd.add_argument("--db", type=Path, default=Path("data/live.sqlite3"))
        cmd.add_argument("--out", type=Path, default=Path("reports/live"))
        cmd.add_argument("--top", type=positive_int, default=20)
        cmd.add_argument("--llm", action="store_true", help="Use configured compatible LLM")
        cmd.add_argument(
            "--llm-top",
            type=positive_int,
            default=3,
            help="Bound model calls to this many eligible report entries",
        )
    live = commands.choices["collect"]
    live.add_argument("--source", choices=["both", "polymarket", "kalshi"], default="both")
    live.add_argument(
        "--limit", type=positive_int, default=100, help="Markets per API page (<=100)"
    )
    live.add_argument("--max-pages", type=positive_int, default=2)
    live.add_argument(
        "--kalshi-series",
        nargs="+",
        default=["KXFEDDECISION", "KXCPI", "KXGDP"],
        help="Default is a macro watchlist. Use ALL for bounded unfiltered discovery.",
    )
    live.add_argument("--timeout", type=float, default=20)
    commands.choices["analyze"].add_argument("--as-of", help="Timezone-aware ISO timestamp")
    live.add_argument(
        "--history-per-source",
        type=int,
        default=0,
        help="Backfill 48h native prices for up to this many eligible markets per venue (0-20)",
    )
    evaluate = commands.add_parser("evaluate", help="Offline labeled scenario and ablation study")
    evaluate.add_argument("--out", type=Path, default=Path("reports/evaluation"))
    evaluate.add_argument("--seed", type=int, default=41)
    evaluate.add_argument("--cases-per-family", type=positive_int, default=12)
    verify = commands.add_parser("verify", help="Verify report artifact checksums")
    verify.add_argument("--dir", type=Path, required=True)
    for cmd in [demo, replay, commands.choices["collect"], commands.choices["analyze"], evaluate]:
        cmd.add_argument("--config", type=Path, help="TOML file with an [analysis] table")
    return parser


def run_report(store, markets, out, as_of, mode, coverage, top=20, llm=False, llm_top=3, cfg=None):
    cfg = cfg or Config()
    natives = {m.key: store.native_for(m, as_of) for m in markets}
    histories = {m.key: store.history(m) for m in markets}
    analyses = [analyze(m, histories[m.key], cfg, as_of, natives[m.key]) for m in markets]
    analyses.sort(key=lambda a: (not a.eligible, -a.score, a.market.key))
    entries, model_calls = [], 0
    for a in analyses[:top]:
        use_llm = llm and a.eligible and model_calls < llm_top
        if use_llm:
            model_calls += 1
        result = judge(a, use_llm)
        history = [
            {
                "observed_at": h.observed_at,
                "probability": h.probability,
                "probability_basis": h.probability_basis,
            }
            for h in histories[a.market.key]
            if h.probability_basis == a.market.probability_basis and h.rules == a.market.rules
        ]
        entries.append(
            {
                "analysis": a.to_dict(),
                "agent": result.to_dict(),
                "history": history,
                "native_history": natives[a.market.key].to_dict()
                if natives[a.market.key]
                else None,
            }
        )
    meta = {
        "as_of": as_of,
        "data_mode": mode,
        "package_version": __version__,
        "coverage": coverage,
        "config": cfg.to_dict(),
        "counts": {
            "processed": len(analyses),
            "eligible": sum(a.eligible for a in analyses),
            "excluded": sum(not a.eligible for a in analyses),
            "reported": len(entries),
        },
        "agent": {
            "requested_mode": "llm" if llm else "rules",
            "max_model_calls": llm_top if llm else 0,
            "attempted_model_calls": model_calls,
            "failed_model_calls": sum(e["agent"]["error"] is not None for e in entries),
        },
        "ranking": "Eligibility first, then descending heuristic research priority; no return forecast.",
        "code_sha256": code_digest(),
        "input_sha256": digest(
            {
                "markets": [m.to_dict() for m in sorted(markets, key=lambda m: m.key)],
                "local_history": {
                    key: [m.to_dict() for m in values] for key, values in histories.items()
                },
                "native_history": {key: h.to_dict() if h else None for key, h in natives.items()},
            }
        ),
        "runtime": {"python": platform.python_version(), "platform": sys.platform},
    }
    if llm:
        import os

        meta["agent"]["model"] = os.environ.get("LLM_MODEL")
        meta["agent"]["response_format"] = os.environ.get("LLM_RESPONSE_FORMAT", "json_schema")
    meta["run_id"] = digest(
        {
            "as_of": as_of,
            "data_mode": mode,
            "config": cfg.to_dict(),
            "code_sha256": meta["code_sha256"],
            "input_sha256": meta["input_sha256"],
            "analyses": [a.to_dict() for a in analyses],
            "agent_mode": "llm" if llm else "rules",
            "agent_model": meta["agent"].get("model"),
            "agent_response_format": meta["agent"].get("response_format"),
            "top": top,
        }
    )[:20]
    summary = write_reports(out, entries, meta)
    write_audit(out, meta, entries)
    print(
        f"{mode}: processed={len(analyses)} eligible={meta['counts']['eligible']} "
        f"reported={summary['markets']} investigate={summary['investigate']} "
        f"monitor={summary['monitor']} abstain={summary['abstain']}"
    )
    print(f"Report: {(out / 'report.html').resolve()}")
    return meta


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)
    if args.command == "collect" and (args.limit > 100 or not 0 < args.timeout <= 120):
        parser.error("--limit must be <=100 and --timeout must be in (0,120]")
    if args.command == "collect" and not 0 <= args.history_per_source <= 20:
        parser.error("--history-per-source must be in [0,20]")
    try:
        if args.command == "verify":
            result = verify_manifest(args.dir)
            print(json.dumps(result))
            return 0 if result["valid"] else 2
        cfg = Config()
        if args.config:
            with args.config.open("rb") as f:
                data = tomllib.load(f)
            if set(data) != {"analysis"}:
                raise ValueError("Configuration must contain exactly one [analysis] table")
            cfg = Config(**data["analysis"])
        if args.command == "evaluate":
            from .evaluation import evaluate

            result = evaluate(args.out, args.seed, args.cases_per_family, cfg)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0
        if args.command == "demo":
            snapshots = demo_snapshots()
            with Store(":memory:") as store:
                store.save(snapshots)
                run_report(
                    store,
                    store.latest(DEMO_AS_OF),
                    args.out,
                    DEMO_AS_OF,
                    "synthetic",
                    {
                        "note": "Generated fixtures; not real markets, history, or LLM responses.",
                        "snapshots": len(snapshots),
                        "markets": 6,
                        "network_calls": 0,
                    },
                    top=6,
                    cfg=cfg,
                )
            write_json(args.out / "snapshots.json", [m.to_dict() for m in snapshots])
            return 0

        if args.command == "replay":
            bundle = json.loads(args.bundle.read_text(encoding="utf-8"))
            as_of = bundle["as_of"]
            parse_time(as_of)
            markets = [Market.from_dict(obj) for obj in bundle["markets"]]
            native = [NativeHistory.from_dict(h) for h in bundle.get("native_history", [])]
            if any(parse_time(m.observed_at) > parse_time(as_of) for m in markets):
                raise ValueError("Bundle includes snapshots after as_of")
            if any(parse_time(h.received_at) > parse_time(as_of) for h in native):
                raise ValueError("Bundle includes history received after as_of")
            with Store(":memory:") as store:
                store.save(markets)
                store.save_native(native)
                run_report(
                    store,
                    store.latest(as_of),
                    args.out,
                    as_of,
                    "captured_api_replay",
                    bundle["coverage"],
                    top=args.top,
                    cfg=cfg,
                )
            return 0

        with Store(args.db) as store:
            if args.command == "collect":
                sources = ["polymarket", "kalshi"] if args.source == "both" else [args.source]
                series = None if args.kalshi_series == ["ALL"] else args.kalshi_series

                def fetch(source):
                    return collect(
                        source, JsonHTTP(timeout=args.timeout), args.limit, args.max_pages, series
                    )

                with ThreadPoolExecutor(max_workers=2) as pool:
                    batches = list(pool.map(fetch, sources))
                markets = [m for b in batches for m in b.markets]
                store.save(markets)
                native, native_raw, native_errors = {}, [], []
                if args.history_per_source:
                    selection_time = utc_now()
                    candidates = [
                        analyze(m, store.history(m), cfg, selection_time) for m in markets
                    ]
                    candidates.sort(key=lambda a: (-a.score, a.market.key))
                    native, native_raw, native_errors = backfill(
                        [a.market for a in candidates if a.eligible],
                        args.history_per_source,
                        JsonHTTP(timeout=args.timeout),
                    )
                    store.save_native(list(native.values()))
                as_of = utc_now()
                raw_dir = args.db.parent / "runs" / parse_time(as_of).strftime("%Y%m%dT%H%M%S%fZ")
                coverage = {
                    "sources": [
                        {k: v for k, v in b.to_dict().items() if k != "raw_pages"} for b in batches
                    ],
                    "kalshi_series": series or "ALL (bounded page scan)",
                    "page_limit": args.limit,
                    "max_pages_per_scope": args.max_pages,
                    "note": "Polymarket sorted by rolling volume; Kalshi scoped watchlist. "
                    "Not complete exchange coverage. Raw pages saved beside database.",
                    "native_history": {
                        "requested_per_source": args.history_per_source,
                        "series": len(native),
                        "points": sum(len(h.points) for h in native.values()),
                        "errors": native_errors,
                    },
                }
                write_json(raw_dir / "raw.json", [b.to_dict() for b in batches])
                write_json(raw_dir / "normalized.json", [m.to_dict() for m in markets])
                write_json(raw_dir / "native_raw.json", native_raw)
                write_json(raw_dir / "manifest.json", {"as_of": as_of, "coverage": coverage})
                write_json(
                    args.out / "snapshot_bundle.json",
                    {
                        "as_of": as_of,
                        "coverage": coverage,
                        "markets": [h.to_dict() for m in markets for h in store.history(m)],
                        "native_history": [
                            h.to_dict()
                            for m in markets
                            if (h := store.native_for(m, as_of)) is not None
                        ],
                    },
                )
                if not markets:
                    print(
                        f"No markets collected; diagnostics: {raw_dir.resolve()}", file=sys.stderr
                    )
                    return 2
                for b in batches:
                    print(
                        f"{b.source}: {len(b.markets)} normalized, {b.skipped} skipped, "
                        f"errors={len(b.errors)}, truncated={b.truncated}"
                    )
                run_report(
                    store,
                    markets,
                    args.out,
                    as_of,
                    "live_api",
                    coverage,
                    args.top,
                    args.llm,
                    args.llm_top,
                    cfg=cfg,
                )
                return 3 if any(b.errors for b in batches) or native_errors else 0

            as_of = args.as_of or utc_now()
            parse_time(as_of)
            markets = store.latest(as_of)
            if not markets:
                print("No snapshots at this timestamp; run collect first.", file=sys.stderr)
                return 2
            run_report(
                store,
                markets,
                args.out,
                as_of,
                "stored_api_snapshots",
                {
                    "note": "Latest stored snapshot per market at or before as_of; "
                    "markets older than the configured freshness limit are excluded."
                },
                args.top,
                args.llm,
                args.llm_top,
                cfg=cfg,
            )
            return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"Error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
