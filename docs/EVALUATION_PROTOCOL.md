# Evaluation protocol

## Question and predeclared comparison

Does a robust relative-move detector recover injected small changes that fixed absolute thresholds miss, what false alerts remain, and what breaks if risk gates are removed?

Four variants use the same market histories and labels:

1. `fixed_thresholds`: 1h/24h fixed thresholds; risk gates on.
2. `fixed_plus_robust`: add robust hourly-change z; risk gates on.
3. `full_pipeline`: additionally enable rolling-activity surge detection.
4. `without_risk_gates`: deliberately remove the final eligibility gate in the experiment only.

No parameters are selected by the evaluation command. Thresholds are the supplied `Config`. No LLM or network calls run in this study. Run with a configuration file to record deliberate experimental variants rather than editing thresholds silently.

## Dataset and labels

`python -m market_research evaluate` generates 12 scenario families, 12 cases/family/split, 288 total cases. The calibration seed is 41; the holdout seed is 104770. Each split includes both venues. Labels are assigned from the scenario specification before the detector runs:

- Investigate: injected large probability jump, injected small probability jump, injected activity surge.
- Monitor: quiet paths, ordinary high-volatility paths, insufficient history, changed resolution rules and gradual drift.
- Abstain: wide quotes, missing quotes, stale captures and past scheduled closes, each with an injected jump.

The dataset artifact preserves current market metadata, explicit historical observations and labels. Predictions preserve scenario IDs, variant, expected/actual action, feature values and exclusion reasons. The dataset digest and code digest are recorded.

These are **hand-designed synthetic mechanisms**, not human labels of genuine market events. Separate seeds do not create new mechanisms or establish external validity. In particular, labels distinguish injected changes from ordinary generated variation; an operational research desk may choose to review some large ordinary variations too.

## Metrics

Report full three-class confusion matrices and per-class precision/recall/F1, macro F1, ordinary-path false research alerts and expected-abstain cases that were allowed through. Zero-denominator precision/recall/F1 is defined as zero. Every failure remains in JSON; the Markdown report displays the first 20 holdout failures.

## Observed default result

On the 144-case synthetic holdout, fixed thresholds produced macro F1 0.7423, adding robust z produced 0.8615, and the full configuration produced 0.9568. The full configuration still produced **6 false alerts**. Removing risk gates allowed all **48 expected-abstain cases** through.

These results validate and characterize the scenario mechanics. They are not a claim of 95.68% real-market performance, event forecasting accuracy, or financial benefit. The high aggregate score reflects deliberately constructed scenarios; the remaining ordinary-volatility failures are retained rather than tuned away.

## Next decisive experiment

Freeze a real watchlist and a time-based evaluation period. Independently annotate data errors, contract-rule changes, ordinary repricing and unusual repricing before reading detector outputs. Keep a later period untouched while adjusting thresholds on earlier data. Measure the same triage metrics with confidence intervals by venue and report coverage/missingness first.

For the optional model, separately compare summary faithfulness, exact scalar copying, correct abstention, response schema compliance, latency and tokens on identical evidence. The current mocked-model tests establish boundary behavior only, not model quality.
