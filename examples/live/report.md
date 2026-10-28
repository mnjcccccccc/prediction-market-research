# Prediction Market Research

Data mode: **captured_api_replay**
As of: 2026-10-28T08:14:10.807645+00:00 (UTC timestamps)

Research priority only. Prices are market-implied, not independent forecasts.

| Venue | Market | YES | Score | Decision |
|---|---|---:|---:|---|
| polymarket | Will the Democratic Party control the Senate after the 2026 Midterm elections? | 66.5% | 74.5 | monitor |
| polymarket | 2026 Balance of Power: D Senate, D House | 65.5% | 73.8 | monitor |
| polymarket | Will the Republican Party control the Senate after the 2026 Midterm elections? | 33.5% | 73.64 | monitor |
| polymarket | Will AC Milan win on 2026-10-28? | 55.5% | 72.94 | monitor |
| polymarket | US announces end of Iranian blockade by December 31, 2026? | 35.4% | 72.56 | monitor |
| polymarket | Will Marine Le Pen win the 2027 French presidential election? | 43.0% | 72.13 | monitor |
| polymarket | Will Juventus FC win on 2026-10-28? | 53.5% | 72.1 | monitor |
| polymarket | Will Bitcoin reach $82,500 in October? | 60.5% | 71.86 | monitor |
| polymarket | US x Iran ceasefire continues through November 15? | 50.5% | 71.73 | monitor |
| polymarket | Will the Republicans win the Texas Senate race in 2026? | 32.5% | 71.36 | monitor |
| polymarket | Will Puma Shen win the next Taipei Mayor election? | 33.4% | 71.26 | monitor |
| kalshi | Will the Federal Reserve Hike rates by 0bps at their December 2026 meeting? | 22.5% | 71.23 | monitor |

## Data coverage

```json
{
  "sources": [
    {
      "source": "polymarket",
      "normalized_count": 175,
      "skipped": 25,
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
  "note": "Polymarket sorted by rolling volume; Kalshi scoped watchlist. Not complete exchange coverage. Raw pages saved beside database."
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
      "value": 424653.0354889996,
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
      "value": 293897.048222,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 73.8,
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
      "value": 303515.50057200005,
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
      "value": 113650.82221300002,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.94,
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
      "value": 0.3535,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 128512.54476399999,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.0050000000000000044,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.56,
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
      "value": 54253.179513,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.0010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.13,
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
      "value": 0.535,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 77560.231685,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 72.1,
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

## Will Bitcoin reach $82,500 in October?

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
      "value": 0.605,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 93527.97545400001,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.86,
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
      "value": 64740.534700000004,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.73,
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
      "value": 136070.552875,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.010000000000000009,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.36,
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
      "value": 0.334,
      "unit": "probability"
    },
    {
      "evidence_id": "e_volume_24h",
      "value": 107670.316391,
      "unit": "usd"
    },
    {
      "evidence_id": "e_spread",
      "value": 0.008000000000000007,
      "unit": "probability"
    },
    {
      "evidence_id": "e_priority",
      "value": 71.26,
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
