# Validation record — 2026-10-28

## Observed results

- Environment: Windows, Python 3.12.7.
- `python -m pytest -q`: **61 passed**.
- `python -m ruff check .`: **All checks passed**.
- Offline demo: 156 snapshots, 6 synthetic markets; 2 investigate, 1 monitor, 3 abstain.
- Both public production APIs responded without authentication. Final v0.2 capture timestamp: `2026-10-28T08:50:23.924684+00:00`.
- Final live capture: 169 normalized Polymarket markets and 121 Kalshi markets, zero collection/parser errors. 31 non-Yes/No Polymarket rows were intentionally skipped. Polymarket scan stopped at the two-page cap, explicitly reported as `truncated=true`.
- Selection: 112 of 290 normalized markets passed the configured gates. The report includes the top 20, all monitor. Six real native series contain 1,779 points; four series appear in the displayed markets. Backfill errors: zero.
- The original 296-market single-capture example remains in `examples/live`; the new native-history example is `examples/live-v2`. Both support offline replay at acquisition time without creating synthetic market history.
- Synthetic study: 288 cases, 144 holdout; fixed / fixed+robust / full macro F1 = 0.7423 / 0.8615 / 0.9568. Full pipeline retains 6 false alerts. The risk-gate ablation permits 48/48 expected abstentions. These are synthetic mechanics, not real detection accuracy.
- Browser check: report loads; searching real ID `562793` filters to one market and expanding it displays the native price curve, evidence and numeric claims. A saved preview is in `examples/live-v2/preview.png`. The synthetic report preview is also refreshed.
- Clean source ZIP extraction: all source-file SHA256 hashes match the manifest. `python -S` runs demo, native-history replay, verify and evaluate without site packages. All 20 real replay entries match original features, local/native histories and decisions; input digests also match. Measured latency and the explicit live/replay mode label can differ.

The committed HTML/JSON/Markdown are generated artifacts. Later live runs will differ as prices and available markets change. Agent-rule latency is measured locally but is not an LLM benchmark. The test suite exercises model error handling using mocked responses; no paid model was called for this delivery.

## What the tests establish

| Area | Evidence checked |
|---|---|
| Normalization | Yes label lookup, non-binary exclusion, invalid probabilities, dollar/cents precedence, contract units, empty books |
| Collection | Cursor propagation, deduplication, scoped requests, partial-failure preservation |
| Persistence | Idempotent writes, latest-at-timestamp query, exclusion of future snapshots |
| Temporal features | Hourly jump, irregular/missing baselines, changed rules/basis, no future leakage, rolling volume semantics |
| Risk/agent | Wide-spread/expired/unpriced rejection, stale snapshots, unknown evidence and risk-override rejection |
| Model boundary | Failed request abstention without leaking exception text, fabricated evidence rejection |
| Artifacts | Full offline CLI, expected scenario decisions, external HTML text escaping, empty database failure |
| Replay | Original capture time, future-snapshot rejection, invalid deserialized values |
| Native history | YES token order, bid/ask candle basis, candle-volume unit, hourly sample selection, no mixed bases, event/receive-time availability |
| Quantitative boundary | Exact claim value/sign/unit, anomaly requirement, strict-schema request, refusal usage retention, malformed provider-envelope abstention |
| Audit/config | TOML validation, trace role coverage, report mutation detection, code/input identities |
| Evaluation | Independent RNG splits, metric arithmetic, safety-gate ablation, exact capture replay including local prior snapshots |

## Not yet established

No result in this repository establishes real-world anomaly precision, trading profitability, well-calibrated event probabilities, LLM summary accuracy, full exchange coverage, production uptime, or quote freshness. Synthetic scenarios validate mechanics, not financial performance. Different seeds retain the same hand-designed mechanisms. Native backfills lack historical rule versions and cannot establish past knowledge. CI is configured for Linux/Python 3.11–3.13, demo/verify/evaluate, but has not run on GitHub until publication.
