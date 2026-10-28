# Design notes

## Problem and deliverable

The ARTi challenge asks for public Polymarket/Kalshi market ingestion, a useful market-analysis framework, probability tracking and anomaly detection, a simple TradingAgents-inspired judgment layer, and a reproducible README with sample output. This implementation produces a research queue with explicit evidence rather than generating unsupported trading recommendations.

## Why these choices

| Choice | Reason | Cost / next step |
|---|---|---|
| Standard-library runtime | A reviewer can run the demo immediately; small integration surface | Handwritten contracts need maintenance; consider Pydantic once schema complexity increases |
| SQLite snapshots | Inspectable local persistence, unique keys, time-bounded reads | Not a distributed time-series store; add retention and indexing for larger deployments |
| Explicit role functions | Small, inspectable analyst → risk → manager flow | No graph checkpointing or parallel agent reasoning; useful only if workflow complexity warrants it |
| Rules as default | Reproducible, no model key, transparent baseline | No external world knowledge; compare real LLM outputs before making quality claims |
| Optional one-call LLM manager | Limits latency and token cost; native schema plus exact scalar-claim validation | Free text can still misread evidence; real model quality requires separate evaluation |
| Two distinct history paths | Local metadata snapshots plus bounded native price backfills address cold start | Native series lack historical rule versions; never fabricate historical market metadata |
| TOML, hashes and JSONL traces | Reproduce inputs, inspect role outputs and detect accidental report changes | Integrity checks are not signatures; traces are not resumable workflow checkpoints |
| Synthetic ablations | Characterize threshold, robust-z, activity and gate behavior | Hand-designed mechanisms do not establish real-market generalization |
| Separate volume units | Kalshi contract count is not Polymarket dollar turnover | Priority scores remain heuristic; do not interpret them as monetary equivalence |
| No automatic cross-venue joins | Similar titles can have different settlement semantics | Build a reviewed canonical event mapping before comparing executable prices |

## Data contracts

1. Keep both `observed_at` and `source_updated_at`. They answer different questions. Neither proves last trade time.
2. Save raw page payloads, query parameters, timestamps and collection errors alongside normalized data.
3. A local history observation must match `source`, `market_id`, `probability_basis`, `rules`, and `volume_unit` before it can become a delta baseline.
4. Reject non-finite probabilities and counts. Preserve unknowns as null.
5. `source:market_id` is a data identity, not an economic event identity shared across exchanges.
6. Native history preserves exchange `event_time`, acquisition `received_at`, endpoint, parameters and price basis. It is available only after acquisition. A backfill cannot establish knowledge available at its event time.
7. Native deltas compare two native samples, never a current Gamma price against an old CLOB price. Raw native chart points and hourly detector samples have different sampling density. There is no interpolation. Candle volume is not rolling 24h volume.

## Selection and leakage controls

Filtering is a deliberate research-queue decision, not a claim that excluded markets have no information. An overdue scheduled close, missing two-sided book, extremely low/high probability, low rolling activity, missing rules, or stale locally captured snapshot causes abstention.

The database history query applies `ts <= current.observed_at`. Feature computation applies the same constraint defensively. Point-in-time analysis reads the latest observation per market at or before the requested timestamp. Freshness is measured against that analysis timestamp. Offline replay uses the capture timestamp, so a saved historical report remains reproducible later without pretending to be live.

The latest candidate return is excluded from the MAD baseline. Irregular observations are not treated as hourly samples. First-run missing history must not be interpreted as zero market movement.

## Model boundary

Only the final research manager can call a configured language model. Analyst findings and risk blocks are deterministic. The system prompt explicitly treats market titles and rules as untrusted data. The provider receives a strict JSON Schema by default; JSON-object compatibility is an explicit option. The local validator enforces action vocabulary, known evidence IDs, exact structured scalar values/signs/units and risk gates. Investigate requires a detected signal. Failed, malformed, refused or truncated responses become observable abstentions. Returned usage survives rejected output. No model response executes tools or submits orders.

These controls are not a semantic factuality proof. Structured claims can be exact while prose is misleading. A production evaluator should check unsupported causal claims, prose faithfulness, source quality and appropriate abstention with labeled cases. The current delivery exercises provider boundaries with mocks, not paid-model quality experiments.

## Experiments and audit boundaries

The evaluation command runs 288 synthetic cases across 12 scenario families, two RNG seeds and four variants. Its protocol and limitations are in EVALUATION_PROTOCOL.md. All failures are retained. It establishes mechanical behavior on specified mechanisms, not genuine alert precision.

Reports include a code digest, input digest, configuration, input-derived run ID, prompt/schema digests and per-role JSONL trace. The ID identifies input conditions, not a unique stochastic generation. Atomic file writes reduce incomplete artifacts; the manifest checks a fixed set of report files. It provides integrity checking, not authenticity or trusted timestamps. No LangGraph recovery mechanism is implemented.

## Next minimum experiment

Collect at least 48 hours of hourly snapshots for a fixed, documented watchlist. Before tuning, label a held-out set of events for feed gaps, contract-rule changes, wide spreads, ordinary repricing and unusual repricing. Compare fixed jump thresholds against the MAD rule on precision of review alerts and missed labeled events, including performance by venue. Report coverage and missing-data rate before reporting any detection metric.

Separately evaluate rules versus one-call LLM summaries on evidence faithfulness, appropriate abstention, latency and tokens. Keep the same evidence and label rubric. Do not use settled outcomes alone as the label for whether an earlier anomaly warranted investigation; that is a different task.

After those tests, consider order-book depth, historical rule versions, canonical event mappings and news retrieval with point-in-time provenance. Any return experiment would additionally require fees, slippage, trade timing and an execution model. Primary-source comparisons and the explicit choice to retain a small standard-library runtime are documented in REFERENCE_REVIEW.md.
