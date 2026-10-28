# Changelog

## 0.2.0 — 2026-10-28

- Added bounded, read-only Polymarket price-history and Kalshi hourly-candle backfills, with separate event/receive timestamps and source-specific price bases.
- Kept native history separate from local market snapshots; added offline replay of both and point-in-time availability checks.
- Added 288 labeled synthetic cases, calibration/holdout RNG seeds, four ablations, confusion matrices and retained failures.
- Added provider-native JSON Schema, exact structured numeric-claim/unit checks, supported-action checks and observable refusal/truncation handling.
- Added validated TOML analysis configuration, input/code hashes, input-derived run IDs, role JSONL traces, atomic writes and report checksum verification.
- Corrected expiry screening to use analysis time and freshness screening to use unrounded time differences.
- Expanded regression tests and updated the submission materials after primary-source review.

## 0.1.0

Initial challenge implementation: public adapters, local SQLite history, selection/anomaly rules, a simple role pipeline, offline demo and first real capture.
