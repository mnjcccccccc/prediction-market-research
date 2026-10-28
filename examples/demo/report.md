# Prediction Market Research

Data mode: **synthetic**
As of: 2026-10-28T08:00:00+00:00 (UTC timestamps)

Research priority only. Prices are market-implied, not independent forecasts.

| Venue | Market | YES | Score | Decision |
|---|---|---:|---:|---|
| kalshi | [SYNTHETIC] BTC above threshold? | 52.0% | 89.98 | investigate |
| polymarket | [SYNTHETIC] Rate cut at next meeting? | 54.0% | 81.1 | investigate |
| kalshi | [SYNTHETIC] CPI exceeds 2.5%? | 50.0% | 68.23 | monitor |
| kalshi | [SYNTHETIC] Expired event? | 60.0% | 62.61 | abstain |
| polymarket | [SYNTHETIC] Growth exceeds 3%? | 50.0% | 46.58 | abstain |
| polymarket | [SYNTHETIC] New unpriced event? | N/A | 0.0 | abstain |

## Data coverage

```json
{
  "note": "Generated fixtures; not real markets, history, or LLM responses.",
  "snapshots": 156,
  "markets": 6,
  "network_calls": 0
}
```

## Limitations

- Bounded REST sampling, not complete exchange coverage or a real-time stream.
- Unavailable time-matched history is reported as null, never fabricated.
- Rolling-volume ratios do not measure interval volume.
- No automatic cross-venue matching, executable arbitrage, or profitability claim.
- Model evidence IDs are validated; semantic factuality still needs human review.

## [SYNTHETIC] BTC above threshold?

Prioritize human review. YES changed +13.00 pp over 1.00h. YES changed +12.80 pp over 24.00h. Rolling-24h volume is 6.00x its day-ago level. Hourly move robust z=26.00; 24 prior moves.

```json
{
  "action": "investigate",
  "priority": "high",
  "summary": "Prioritize human review. YES changed +13.00 pp over 1.00h. YES changed +12.80 pp over 24.00h. Rolling-24h volume is 6.00x its day-ago level. Hourly move robust z=26.00; 24 prior moves.",
  "evidence_ids": [
    "e_change_1h",
    "e_change_24h",
    "e_robust_z",
    "e_volume_ratio",
    "e_quality",
    "e_spread",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_change_1h",
      "value": 0.13,
      "unit": "probability"
    },
    {
      "evidence_id": "e_change_24h",
      "value": 0.128,
      "unit": "probability"
    },
    {
      "evidence_id": "e_robust_z",
      "value": 26.0,
      "unit": "robust_standardized_hourly_move"
    },
    {
      "evidence_id": "e_volume_ratio",
      "value": 6.0,
      "unit": "ratio"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.020000000000000018,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 89.98,
      "unit": "score"
    }
  ],
  "risks": [
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```

## [SYNTHETIC] Rate cut at next meeting?

Prioritize human review. YES changed +9.20 pp over 1.00h. Hourly move robust z=18.00; 24 prior moves.

```json
{
  "action": "investigate",
  "priority": "high",
  "summary": "Prioritize human review. YES changed +9.20 pp over 1.00h. Hourly move robust z=18.00; 24 prior moves.",
  "evidence_ids": [
    "e_change_1h",
    "e_robust_z",
    "e_quality",
    "e_spread",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_change_1h",
      "value": 0.092,
      "unit": "probability"
    },
    {
      "evidence_id": "e_robust_z",
      "value": 18.0,
      "unit": "robust_standardized_hourly_move"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.020000000000000018,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 81.1,
      "unit": "score"
    }
  ],
  "risks": [
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```

## [SYNTHETIC] CPI exceeds 2.5%?

Eligible for monitoring; available evidence does not cross anomaly thresholds.

```json
{
  "action": "monitor",
  "priority": "normal",
  "summary": "Eligible for monitoring; available evidence does not cross anomaly thresholds.",
  "evidence_ids": [
    "e_probability",
    "e_volume_24h",
    "e_quality",
    "e_spread",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_probability",
      "value": 0.5,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 5000.0,
      "unit": "contracts"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.020000000000000018,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 68.23,
      "unit": "score"
    }
  ],
  "risks": [
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```

## [SYNTHETIC] Expired event?

Excluded by data-quality or market-quality gates: past_scheduled_close

```json
{
  "action": "abstain",
  "priority": "low",
  "summary": "Excluded by data-quality or market-quality gates: past_scheduled_close",
  "evidence_ids": [
    "e_probability",
    "e_volume_24h",
    "e_quality",
    "e_spread",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_probability",
      "value": 0.6,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 1000.0,
      "unit": "contracts"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.020000000000000018,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 62.61,
      "unit": "score"
    }
  ],
  "risks": [
    "past_scheduled_close",
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```

## [SYNTHETIC] Growth exceeds 3%?

Excluded by data-quality or market-quality gates: wide_spread

```json
{
  "action": "abstain",
  "priority": "low",
  "summary": "Excluded by data-quality or market-quality gates: wide_spread",
  "evidence_ids": [
    "e_spread",
    "e_quality",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_spread",
      "value": 0.30000000000000004,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 46.58,
      "unit": "score"
    }
  ],
  "risks": [
    "wide_spread",
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```

## [SYNTHETIC] New unpriced event?

Excluded by data-quality or market-quality gates: missing_probability, insufficient_24h_activity, missing_two_sided_quote

```json
{
  "action": "abstain",
  "priority": "low",
  "summary": "Excluded by data-quality or market-quality gates: missing_probability, insufficient_24h_activity, missing_two_sided_quote",
  "evidence_ids": [
    "e_probability",
    "e_volume_24h",
    "e_quality",
    "e_spread",
    "e_rules",
    "e_priority"
  ],
  "claims": [
    {
      "evidence_id": "e_priority",
      "value": 0.0,
      "unit": "score"
    }
  ],
  "risks": [
    "missing_probability",
    "insufficient_24h_activity",
    "missing_two_sided_quote",
    "missing_or_invalid_probability",
    "Market-implied price is not an independent fair-value estimate.",
    "No news verification or order-book depth assessment is included.",
    "Source metadata timestamp does not prove quote freshness."
  ],
  "next_steps": [
    "Read the exact resolution rules and verify against the official primary source.",
    "Collect further time-stamped snapshots before interpreting a price move.",
    "Inspect executable quotes and depth; research priority is not a trading edge."
  ]
}
```
