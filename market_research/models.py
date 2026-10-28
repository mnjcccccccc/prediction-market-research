"""Normalized, serializable contracts. Missing numbers remain None, never zero-filled."""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import math
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def parse_time(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        raise ValueError("Timestamps must include a timezone")
    return dt.astimezone(timezone.utc)


def number(value: Any) -> float | None:
    if value is None or value == "" or isinstance(value, bool):
        return None
    try:
        result = float(value)
    except (ValueError, TypeError):
        return None
    return result if math.isfinite(result) else None


def nonnegative(value: Any) -> float | None:
    n = number(value)
    return n if n is not None and n >= 0 else None


def probability(value: Any) -> float | None:
    n = number(value)
    return n if n is not None and 0 <= n <= 1 else None


@dataclass
class Market:
    source: str
    market_id: str
    title: str
    observed_at: str
    source_updated_at: str | None
    close_time: str | None
    active: bool
    probability: float | None
    probability_basis: str
    yes_bid: float | None
    yes_ask: float | None
    volume_24h: float | None
    volume_total: float | None
    volume_unit: str
    liquidity_usd: float | None
    rules: str
    url: str
    issues: list[str] = field(default_factory=list)
    yes_token_id: str | None = None
    series_ticker: str | None = None

    @property
    def key(self) -> str:
        return f"{self.source}:{self.market_id}"

    @property
    def spread(self) -> float | None:
        if self.yes_bid is None or self.yes_ask is None:
            return None
        if self.yes_bid > self.yes_ask:
            return None
        return self.yes_ask - self.yes_bid

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: dict) -> "Market":
        m = cls(**obj)
        if m.source not in {"polymarket", "kalshi"} or not isinstance(m.market_id, str):
            raise ValueError("Invalid market identity")
        for name in ("market_id", "title", "rules", "url", "probability_basis"):
            if not isinstance(getattr(m, name), str):
                raise ValueError(f"{name} must be a string")
        if not m.market_id or not m.title or not isinstance(m.active, bool):
            raise ValueError("Invalid market identity or active flag")
        if not isinstance(m.issues, list) or any(not isinstance(i, str) for i in m.issues):
            raise ValueError("Issues must be strings")
        for name in ("yes_token_id", "series_ticker"):
            if getattr(m, name) is not None and not isinstance(getattr(m, name), str):
                raise ValueError(f"Invalid {name}")
        parse_time(m.observed_at)
        for name in ("probability", "yes_bid", "yes_ask"):
            value = getattr(m, name)
            if value is not None and probability(value) is None:
                raise ValueError(f"Invalid {name}")
            if value is not None and not isinstance(value, (int, float)):
                raise ValueError(f"{name} must be a JSON number")
        for name in ("volume_24h", "volume_total", "liquidity_usd"):
            value = getattr(m, name)
            if value is not None and (
                nonnegative(value) is None or not isinstance(value, (int, float))
            ):
                raise ValueError(f"Invalid {name}")
        if m.volume_unit != {"polymarket": "usd", "kalshi": "contracts"}[m.source]:
            raise ValueError("Unexpected volume unit")
        return m


@dataclass
class Signal:
    kind: str
    severity: str
    evidence_ids: list[str]
    description: str


@dataclass
class Analysis:
    market: Market
    eligible: bool
    exclusion_reasons: list[str]
    score: float
    evidence: dict[str, Any]
    signals: list[Signal]

    def to_dict(self) -> dict:
        return asdict(self)
