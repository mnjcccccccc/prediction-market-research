# ARTi Challenge Submission

**Position:** AI Research Engineer  
**Challenge:** Prediction market data source + analysis framework

This repository provides public Polymarket and Kalshi adapters, SQLite snapshots, native price-history backfills, time-matched anomaly detection, and a TradingAgents-inspired analyst/risk/manager judgment layer. Decisions have checked evidence and quantitative claims. It includes portable reports, per-role traces, integrity manifests and a four-variant synthetic evaluation. A compatible model can optionally summarize evidence; the rule baseline runs without credentials.

Suggested review path:

1. Run `python -m market_research demo` and open `reports/demo/report.html`.
2. Replay real captured data and native history with `python -m market_research replay --bundle examples/live-v2/snapshot_bundle.json`.
3. Read `README.md` for the schema, methods, data units and sample output.
4. Run `python -m market_research evaluate` and inspect retained failures; read `docs/EVALUATION_PROTOCOL.md` before interpreting metrics.
5. Inspect `native_history.py`, `analysis.py`, `agents.py` and `audit.py`; run `python -m market_research verify --dir reports/replay`.
6. Run the 61 tests; review `docs/REFERENCE_REVIEW.md`, `docs/DESIGN.md` and `docs/VALIDATION.md` for sources, tradeoffs and limits.

The final live sample was captured on 2026-10-28: 290 normalized markets and six native series with 1,779 points. Missing history remains unknown. Native price data and local metadata snapshots remain separate; acquisition time limits retrospective availability. The 288-case study is explicitly synthetic, not independent real-market accuracy. No return or LLM-quality claims are made.

The applicant's resume is supplied separately with the application email.
