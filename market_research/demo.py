"""Fixed, explicitly SYNTHETIC fixtures for reproducible end-to-end review."""

from datetime import datetime, timedelta, timezone

from .adapters import kalshi, polymarket

DEMO_AS_OF = "2026-10-28T08:00:00+00:00"


def demo_snapshots():
    start = datetime(2026, 10, 27, 7, tzinfo=timezone.utc)
    markets = []
    for hour in range(26):
        observed = (start + timedelta(hours=hour)).isoformat()
        # Regular small moves, followed by an injected final-hour jump.
        rate_p = 0.45 + (hour % 3 - 1) * 0.002 if hour < 25 else 0.54
        crypto_p = 0.39 + (hour % 2) * 0.002 if hour < 25 else 0.52
        poly_rows = [
            {
                "id": "DEMO-POLY-RATES",
                "question": "[SYNTHETIC] Rate cut at next meeting?",
                "outcomes": ["No", "Yes"],
                "outcomePrices": [1 - rate_p, rate_p],
                "bestBid": rate_p - 0.01,
                "bestAsk": rate_p + 0.01,
                "volume24hr": 24000,
                "liquidityNum": 12000,
            },
            {
                "id": "DEMO-POLY-WIDE",
                "question": "[SYNTHETIC] Growth exceeds 3%?",
                "outcomes": ["Yes", "No"],
                "outcomePrices": [0.5, 0.5],
                "bestBid": 0.35,
                "bestAsk": 0.65,
                "volume24hr": 5000,
                "liquidityNum": 500,
            },
            {
                "id": "DEMO-POLY-MISSING",
                "question": "[SYNTHETIC] New unpriced event?",
                "outcomes": ["Yes", "No"],
                "outcomePrices": [None, None],
                "volume24hr": None,
                "liquidityNum": None,
            },
        ]
        for row in poly_rows:
            row.update(
                active=True,
                closed=False,
                updatedAt=observed,
                endDate="2026-12-31T23:59:00Z",
                volume=100000 + hour * 1000,
                description="SYNTHETIC TEST RULES: resolves YES if the stated threshold "
                "is met in the imaginary official release. No real event.",
            )
            m = polymarket(row, observed)
            m.url = ""
            markets.append(m)
        kalshi_rows = [
            {
                "ticker": "DEMO-KALSHI-CPI",
                "title": "[SYNTHETIC] CPI exceeds 2.5%?",
                "yes_bid_dollars": "0.49",
                "yes_ask_dollars": "0.51",
                "last_price_dollars": "0.50",
                "volume_24h_fp": "5000.00",
            },
            {
                "ticker": "DEMO-KALSHI-CRYPTO",
                "title": "[SYNTHETIC] BTC above threshold?",
                "yes_bid_dollars": str(crypto_p - 0.01),
                "yes_ask_dollars": str(crypto_p + 0.01),
                "last_price_dollars": str(crypto_p),
                "volume_24h_fp": "9000.00" if hour == 25 else "1500.00",
            },
            {
                "ticker": "DEMO-KALSHI-CLOSED",
                "title": "[SYNTHETIC] Expired event?",
                "yes_bid_dollars": "0.59",
                "yes_ask_dollars": "0.61",
                "last_price_dollars": "0.60",
                "volume_24h_fp": "1000.00",
            },
        ]
        for row in kalshi_rows:
            row.update(
                market_type="binary",
                status="active",
                event_ticker="DEMO-EVENT",
                close_time="2026-12-31T23:59:00Z",
                updated_time=observed,
                volume_fp=str(100000 + hour * 1000),
                yes_bid_size_fp="100.00",
                yes_ask_size_fp="100.00",
                rules_primary="SYNTHETIC TEST RULES: threshold in an imaginary release.",
            )
            if row["ticker"].endswith("CLOSED"):
                row["close_time"] = "2026-10-26T00:00:00Z"
            m = kalshi(row, observed)
            m.url = ""
            markets.append(m)
    return markets
