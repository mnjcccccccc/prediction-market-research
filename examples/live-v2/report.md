# Prediction Market Research

Data mode: **live_api**
As of: 2026-10-28T08:50:23.924684+00:00 (UTC timestamps)

Research priority only. Prices are market-implied, not independent forecasts.

| Venue | Market | YES | Score | Decision |
|---|---|---:|---:|---|
| polymarket | Will the Democratic Party control the Senate after the 2026 Midterm elections? | 66.5% | 74.5 | monitor |
| polymarket | 2026 Balance of Power: D Senate, D House | 65.5% | 73.81 | monitor |
| polymarket | Will the Republican Party control the Senate after the 2026 Midterm elections? | 33.5% | 73.64 | monitor |
| polymarket | US announces end of Iranian blockade by December 31, 2026? | 35.0% | 73.08 | monitor |
| polymarket | Will AC Milan win on 2026-10-28? | 55.5% | 72.93 | monitor |
| polymarket | Will Juventus FC win on 2026-10-28? | 54.5% | 72.69 | monitor |
| polymarket | Will Marine Le Pen win the 2027 French presidential election? | 43.0% | 72.21 | monitor |
| polymarket | US x Iran ceasefire continues through November 15? | 50.5% | 71.83 | monitor |
| polymarket | Will the Republicans win the Texas Senate race in 2026? | 32.5% | 71.3 | monitor |
| kalshi | Will the Federal Reserve Hike rates by 0bps at their December 2026 meeting? | 22.5% | 71.23 | monitor |
| polymarket | Will Gen.G win Worlds 2026? | 43.5% | 71.04 | monitor |
| polymarket | Will Puma Shen win the next Taipei Mayor election? | 33.6% | 70.9 | monitor |
| polymarket | Will Chiang Wan-an win the next Taipei Mayor election? | 66.5% | 70.7 | monitor |
| polymarket | Russia x Ukraine ceasefire agreement by March 31, 2027? | 35.5% | 70.69 | monitor |
| polymarket | Will the Democrats win the Kansas Senate race in 2026? | 38.5% | 69.62 | monitor |
| polymarket | Will Israel strike 4 countries in 2026? | 66.9% | 69.43 | monitor |
| polymarket | Will the Democrats win the Texas Senate race in 2026? | 67.5% | 69.25 | monitor |
| polymarket | Pete Hegseth out as Secretary of Defense by December 31? | 33.5% | 69.07 | monitor |
| polymarket | Will the Democrats win the Michigan Senate race in 2026? | 69.5% | 68.92 | monitor |
| polymarket | Will the Republican Party win the NC-13 House seat? | 64.5% | 68.9 | monitor |

## Data coverage

```json
{
  "sources": [
    {
      "source": "polymarket",
      "normalized_count": 169,
      "skipped": 31,
      "truncated": true,
      "errors": []
    },
    {
      "source": "kalshi",
      "normalized_count": 121,
      "skipped": 0,
      "truncated": false,
      "errors": []
    }
  ],
  "kalshi_series": [
    "KXFEDDECISION",
    "KXCPI",
    "KXGDP"
  ],
  "page_limit": 100,
  "max_pages_per_scope": 2,
  "note": "Polymarket sorted by rolling volume; Kalshi scoped watchlist. Not complete exchange coverage. Raw pages saved beside database.",
  "native_history": {
    "requested_per_source": 3,
    "series": 6,
    "points": 1779,
    "errors": []
  }
}
```

## Limitations

- Bounded REST sampling, not complete exchange coverage or a real-time stream.
- Unavailable time-matched history is reported as null, never fabricated.
- Rolling-volume ratios do not measure interval volume.
- No automatic cross-venue matching, executable arbitrage, or profitability claim.
- Model evidence IDs are validated; semantic factuality still needs human review.

## Will the Democratic Party control the Senate after the 2026 Midterm elections?

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
      "value": 0.665,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 425567.5121569996,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 74.5,
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

## 2026 Balance of Power: D Senate, D House

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
      "value": 0.655,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 294189.472466,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 73.81,
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

## Will the Republican Party control the Senate after the 2026 Midterm elections?

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
      "value": 0.335,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 302952.96645500005,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 73.64,
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

## US announces end of Iranian blockade by December 31, 2026?

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
      "value": 0.3505,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 130968.84556800002,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.0010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 73.08,
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

## Will AC Milan win on 2026-10-28?

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
      "value": 0.555,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 113202.64222100002,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.93,
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

## Will Juventus FC win on 2026-10-28?

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
      "value": 0.545,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 100242.486041,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.69,
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

## Will Marine Le Pen win the 2027 French presidential election?

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
      "value": 0.4305,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 55803.47177,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.0010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.21,
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

## US x Iran ceasefire continues through November 15?

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
      "value": 0.505,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 67415.53393,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.83,
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

## Will the Republicans win the Texas Senate race in 2026?

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
      "value": 0.325,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 133031.14110999997,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.3,
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

## Will the Federal Reserve Hike rates by 0bps at their December 2026 meeting?

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
      "value": 0.225,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 57794.73,
      "unit": "contracts"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.23,
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

## Will Gen.G win Worlds 2026?

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
      "value": 0.435,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 55558.091453,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.04,
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

## Will Puma Shen win the next Taipei Mayor election?

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
      "value": 0.3355,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 107730.316391,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.01100000000000001,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 70.9,
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

## Will Chiang Wan-an win the next Taipei Mayor election?

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
      "value": 0.665,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 95022.063388,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 70.7,
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

## Russia x Ukraine ceasefire agreement by March 31, 2027?

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
      "value": 0.355,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 78780.934503,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 70.69,
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

## Will the Democrats win the Kansas Senate race in 2026?

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
      "value": 0.385,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 41120.740106,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 69.62,
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

## Will Israel strike 4 countries in 2026?

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
      "value": 0.669,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 81959.587594,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.016000000000000014,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 69.43,
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

## Will the Democrats win the Texas Senate race in 2026?

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
      "value": 0.675,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 59203.713471999996,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 69.25,
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

## Pete Hegseth out as Secretary of Defense by December 31?

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
      "value": 0.335,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 49951.28458099999,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 69.07,
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

## Will the Democrats win the Michigan Senate race in 2026?

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
      "value": 0.695,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 64893.193769,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 68.92,
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

## Will the Republican Party win the NC-13 House seat?

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
      "value": 0.645,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 38839.69011,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 68.9,
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
