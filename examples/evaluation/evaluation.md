# Synthetic stress evaluation

**Not real-market accuracy. No LLM was called.**

Seed: 41; holdout seed: 104770; dataset SHA-256: `b44d2ef7ccf9600b2ed9833f48aab443e9a4e33065af4bd55965d2915f0dc9cb`.
Total labeled cases: 288; 12 families; 12 cases/family/split; 1152 variant decisions.

Labels follow injected regime-change and data-quality scenarios, independently of detector output.
The same family generators are shared across splits; this is not real-world external validation.

## calibration

| Variant | Macro F1 | Alert precision | Alert recall | Unsafe non-abstain | False alerts |
|---|---:|---:|---:|---:|---:|
| fixed_thresholds | 0.742 | 0.667 | 0.333 | 0 | 6 |
| fixed_plus_robust | 0.862 | 0.800 | 0.667 | 0 | 6 |
| full_pipeline | 0.957 | 0.857 | 1.000 | 0 | 6 |
| without_risk_gates | 0.506 | 0.400 | 1.000 | 48 | 6 |

## holdout

| Variant | Macro F1 | Alert precision | Alert recall | Unsafe non-abstain | False alerts |
|---|---:|---:|---:|---:|---:|
| fixed_thresholds | 0.742 | 0.667 | 0.333 | 0 | 6 |
| fixed_plus_robust | 0.862 | 0.800 | 0.667 | 0 | 6 |
| full_pipeline | 0.957 | 0.857 | 1.000 | 0 | 6 |
| without_risk_gates | 0.506 | 0.400 | 1.000 | 48 | 6 |

## Failure cases from the full pipeline

Every error is retained in evaluation.json. First 20 holdout failures:

| Case | Expected | Actual | Signals |
|---|---|---|---|
| holdout/ordinary_high_volatility/000 | monitor | investigate | probability_jump_24h |
| holdout/ordinary_high_volatility/001 | monitor | investigate | probability_jump_24h |
| holdout/ordinary_high_volatility/004 | monitor | investigate | probability_jump_24h |
| holdout/ordinary_high_volatility/008 | monitor | investigate | probability_jump_24h |
| holdout/ordinary_high_volatility/009 | monitor | investigate | probability_jump_24h |
| holdout/ordinary_high_volatility/011 | monitor | investigate | probability_jump_24h |

## Interpretation and next experiment

Fixed thresholds can miss small shifts in quiet markets; a robust relative detector can recover some of them. Ordinary high-volatility paths can also cross the fixed 24h threshold, so higher recall may come with extra review alerts. The labels deliberately distinguish injected shifts from ordinary variation; inspect that mismatch before tuning.

Risk-gate ablation shows what happens when invalid inputs are allowed through. Neither this result nor a high synthetic F1 establishes financial value.

Next: annotate a fixed real watchlist for feed gaps, ordinary repricing and unusual repricing, freeze a time-based held-out period, and compare with the same metrics.

## Limits

- Hand-designed synthetic generators and labels, not independent market annotations.
- A held-out RNG seed tests robustness within generators, not out-of-distribution generalization.
- No parameters were tuned by this evaluation command; inspect failures, not just averages.
- No LLM, real-market detection accuracy, settlement accuracy or returns are measured.
- The no-risk variant deliberately bypasses gates only inside this experiment.
