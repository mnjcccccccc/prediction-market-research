"""Exchange-specific parsing; no title-based cross-exchange equivalence assumptions."""

from dataclasses import dataclass, field
import json
from urllib.parse import quote

from .models import Market, nonnegative, probability, utc_now
from .transport import APIError, JsonHTTP

POLY_URL = "https://gamma-api.polymarket.com/markets"
KALSHI_URL = "https://api.elections.kalshi.com/trade-api/v2/markets"


def _array(value) -> list:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, list):
        raise ValueError("Expected an array")
    return value


def _quote(bid, ask, issues: list[str]):
    bid, ask = probability(bid), probability(ask)
    if bid is not None and ask is not None and (bid > ask or bid == ask == 0):
        issues.append("invalid_or_empty_quote")
        return None, None
    return bid, ask


def polymarket(raw: dict, observed_at: str) -> Market | None:
    outcomes, prices = _array(raw.get("outcomes", [])), _array(raw.get("outcomePrices", []))
    normalized = [str(x).strip().lower() for x in outcomes]
    # A binary event can contain many separate YES/NO markets. Never treat
    # a multi-outcome market's first outcome as YES.
    if len(normalized) != 2 or set(normalized) != {"yes", "no"}:
        return None
    idx = normalized.index("yes")
    issues: list[str] = []
    if len(prices) != 2:
        issues.append("inconsistent_outcome_prices")
    p = probability(prices[idx]) if idx < len(prices) else None
    if p is None:
        issues.append("missing_or_invalid_probability")
    if len(prices) == 2:
        other = probability(prices[1 - idx])
        if p is not None and other is not None and abs(p + other - 1) > 0.03:
            issues.append("inconsistent_outcome_prices")
    bid, ask = _quote(raw.get("bestBid"), raw.get("bestAsk"), issues)
    tokens = _array(raw.get("clobTokenIds") or [])
    return Market(
        source="polymarket",
        market_id=str(raw["id"]),
        title=raw["question"],
        observed_at=observed_at,
        source_updated_at=raw.get("updatedAt"),
        close_time=raw.get("endDate"),
        active=raw.get("active") is True and not raw.get("closed", False),
        probability=p,
        probability_basis="outcome_price_yes",
        yes_bid=bid,
        yes_ask=ask,
        volume_24h=nonnegative(raw.get("volume24hr")),
        volume_total=nonnegative(raw.get("volume")),
        volume_unit="usd",
        liquidity_usd=nonnegative(raw.get("liquidityNum", raw.get("liquidity"))),
        rules=raw.get("description") or "",
        url="https://polymarket.com/market/" + quote(raw.get("slug") or str(raw["id"])),
        issues=issues,
        yes_token_id=str(tokens[idx]) if len(tokens) == 2 else None,
    )


def _dollars(raw: dict, name: str):
    # Presence, not truthiness: an explicit zero dollar price overrides legacy cents.
    if name + "_dollars" in raw:
        return probability(raw[name + "_dollars"])
    cents = nonnegative(raw.get(name))
    return probability(cents / 100) if cents is not None else None


def kalshi(raw: dict, observed_at: str) -> Market | None:
    if raw.get("market_type", "binary") != "binary" or raw.get("mve_collection_ticker"):
        return None
    issues: list[str] = []
    bid, ask = _quote(_dollars(raw, "yes_bid"), _dollars(raw, "yes_ask"), issues)
    # Empty book sides may have a price sentinel but zero posted size.
    if raw.get("yes_bid_size_fp") is not None and nonnegative(raw["yes_bid_size_fp"]) == 0:
        bid = None
    if raw.get("yes_ask_size_fp") is not None and nonnegative(raw["yes_ask_size_fp"]) == 0:
        ask = None
    if bid is not None and ask is not None:
        p, basis = (bid + ask) / 2, "yes_midpoint"
    else:
        p, basis = _dollars(raw, "last_price"), "last_trade_yes"
        traded = nonnegative(raw.get("volume_fp", raw.get("volume")))
        if traded is None or traded == 0:
            p = None
        issues.append("last_trade_may_be_stale" if p is not None else "missing_probability")
    if not raw.get("rules_primary"):
        issues.append("missing_resolution_rules")
    return Market(
        source="kalshi",
        market_id=raw["ticker"],
        title=raw["title"],
        observed_at=observed_at,
        source_updated_at=raw.get("updated_time"),
        close_time=raw.get("close_time"),
        active=raw.get("status") in {"active", "open"},
        probability=p,
        probability_basis=basis,
        yes_bid=bid,
        yes_ask=ask,
        volume_24h=nonnegative(raw.get("volume_24h_fp", raw.get("volume_24h"))),
        volume_total=nonnegative(raw.get("volume_fp", raw.get("volume"))),
        volume_unit="contracts",
        liquidity_usd=None,
        rules="\n".join(filter(None, [raw.get("rules_primary"), raw.get("rules_secondary")])),
        url="https://kalshi.com/markets/" + quote(raw["event_ticker"].lower()),
        issues=issues,
        series_ticker=raw.get("series_ticker") or raw["event_ticker"].split("-")[0],
    )


@dataclass
class Collection:
    source: str
    markets: list[Market] = field(default_factory=list)
    raw_pages: list[dict] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    skipped: int = 0
    truncated: bool = False

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "normalized_count": len(self.markets),
            "skipped": self.skipped,
            "truncated": self.truncated,
            "errors": self.errors,
            "raw_pages": self.raw_pages,
        }


def collect(
    source: str,
    http: JsonHTTP,
    limit: int = 100,
    max_pages: int = 2,
    series: list[str] | None = None,
) -> Collection:
    result = Collection(source)
    seen: set[str] = set()
    scopes = (series or [None]) if source == "kalshi" else [None]
    endpoint = POLY_URL if source == "polymarket" else KALSHI_URL
    parser = polymarket if source == "polymarket" else kalshi
    for scope in scopes:
        cursor = ""
        seen_cursors: set[str] = set()
        for page in range(max_pages):
            params = {"limit": limit}
            if source == "polymarket":
                params.update(
                    active="true",
                    closed="false",
                    offset=page * limit,
                    order="volume24hr",
                    ascending="false",
                )
            else:
                params.update(status="open", mve_filter="exclude")
                if scope:
                    params["series_ticker"] = scope
                if cursor:
                    params["cursor"] = cursor
            try:
                payload = http.get(endpoint, params)
                observed_at = utc_now()
                rows = payload if source == "polymarket" else payload["markets"]
                if not isinstance(rows, list):
                    raise ValueError("Market response is not a list")
                result.raw_pages.append(
                    {
                        "endpoint": endpoint,
                        "params": params,
                        "observed_at": observed_at,
                        "payload": payload,
                    }
                )
                for raw in rows:
                    try:
                        market = parser(raw, observed_at)
                        if market is None:
                            result.skipped += 1
                        elif market.key not in seen:
                            market = Market.from_dict(market.to_dict())
                            result.markets.append(market)
                            seen.add(market.key)
                    except (KeyError, ValueError, TypeError, AttributeError) as exc:
                        result.skipped += 1
                        result.errors.append(f"Malformed market: {type(exc).__name__}")
                if source == "kalshi":
                    cursor = payload.get("cursor", "")
                    more = bool(cursor)
                    if cursor and cursor in seen_cursors:
                        result.errors.append("Repeated pagination cursor; stopped")
                        result.truncated = True
                        break
                    seen_cursors.add(cursor)
                else:
                    more = len(rows) == limit
                if not more:
                    break
                if page == max_pages - 1:
                    result.truncated = True
            except (APIError, KeyError, ValueError, TypeError) as exc:
                result.errors.append(f"Scope {scope or 'all'} page {page}: {exc}")
                break
    return result
