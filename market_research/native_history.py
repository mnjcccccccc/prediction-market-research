"""Exchange-native price series, kept distinct from locally observed market snapshots.

event_time is the exchange sample/candle time; received_at is when we obtained
the series. Backfilled metadata is not evidence of what was known at event_time.
"""

from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
import statistics
from urllib.parse import quote

from .models import Market, nonnegative, parse_time, probability, utc_now
from .transport import APIError, JsonHTTP


@dataclass(frozen=True)
class PricePoint:
    event_time: str
    probability: float
    interval_volume: float | None = None
    volume_unit: str | None = None


@dataclass
class NativeHistory:
    source: str
    market_id: str
    basis: str
    received_at: str
    endpoint: str
    params: dict
    points: list[PricePoint]
    issues: list[str] = field(default_factory=list)

    @property
    def key(self):
        return f"{self.source}:{self.market_id}"

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, obj):
        data = dict(obj)
        data["points"] = [PricePoint(**p) for p in data["points"]]
        result = cls(**data)
        parse_time(result.received_at)
        previous = None
        for p in result.points:
            stamp = parse_time(p.event_time)
            if (
                probability(p.probability) is None
                or isinstance(p.probability, bool)
                or not isinstance(p.probability, (int, float))
            ):
                raise ValueError("Invalid history probability")
            if previous is not None and stamp <= previous:
                raise ValueError("History points must have strictly increasing timestamps")
            if stamp > parse_time(result.received_at):
                raise ValueError("History point is in the future")
            if p.interval_volume is not None and nonnegative(p.interval_volume) is None:
                raise ValueError("Invalid interval volume")
            previous = stamp
        if result.source not in {"kalshi", "polymarket"}:
            raise ValueError("Unknown history source")
        return result


def _stamp(epoch):
    if isinstance(epoch, bool) or not isinstance(epoch, (int, float)):
        raise ValueError("Invalid exchange timestamp")
    return datetime.fromtimestamp(epoch, timezone.utc).isoformat()


def fetch_history(m: Market, http: JsonHTTP, hours: int = 48) -> tuple[NativeHistory, dict]:
    end = int(parse_time(m.observed_at).timestamp())
    start = end - hours * 3600
    if m.source == "polymarket":
        if not m.yes_token_id:
            raise ValueError("Missing YES token ID; recollect market metadata")
        endpoint = "https://clob.polymarket.com/prices-history"
        params = {"market": m.yes_token_id, "startTs": start, "endTs": end, "fidelity": 5}
        basis = "clob_reported_yes_price"
    else:
        if not m.series_ticker:
            raise ValueError("Missing Kalshi series ticker")
        endpoint = (
            "https://api.elections.kalshi.com/trade-api/v2/series/"
            + quote(m.series_ticker, safe="")
            + "/markets/"
            + quote(m.market_id, safe="")
            + "/candlesticks"
        )
        params = {"start_ts": start, "end_ts": end, "period_interval": 60}
        basis = "candle_close_yes_midpoint"
    payload = http.get(endpoint, params)
    received_at = utc_now()
    rows = payload["history" if m.source == "polymarket" else "candlesticks"]
    if not isinstance(rows, list):
        raise ValueError("History response must contain a list")
    points, invalid = {}, 0
    for raw in rows:
        try:
            epoch = raw["t" if m.source == "polymarket" else "end_period_ts"]
            event_time = _stamp(epoch)
            if not start <= epoch <= end:
                invalid += 1
                continue
            volume = None
            if m.source == "polymarket":
                p = probability(raw["p"])
            else:
                bid = probability(raw["yes_bid"].get("close_dollars"))
                ask = probability(raw["yes_ask"].get("close_dollars"))
                p = (
                    (bid + ask) / 2
                    if (bid is not None and ask is not None and 0 < bid <= ask < 1)
                    else None
                )
                volume = nonnegative(raw.get("volume_fp"))
            if p is None:
                invalid += 1
                continue
            points[event_time] = PricePoint(
                event_time, p, volume, "contracts" if volume is not None else None
            )
        except (KeyError, ValueError, TypeError, AttributeError, OSError, OverflowError):
            invalid += 1
    issues = [f"ignored_invalid_or_out_of_window_points:{invalid}"] if invalid else []
    series = NativeHistory(
        m.source,
        m.market_id,
        basis,
        received_at,
        endpoint,
        params,
        sorted(points.values(), key=lambda p: parse_time(p.event_time)),
        issues,
    )
    return series, {
        "source": m.source,
        "market_id": m.market_id,
        "received_at": received_at,
        "endpoint": endpoint,
        "params": params,
        "payload": payload,
    }


def backfill(markets: list[Market], per_source: int, http: JsonHTTP):
    """Bound public requests. Input order is research rank, not API listing order."""
    result, raw, errors = {}, [], []
    counts = {"polymarket": 0, "kalshi": 0}
    for m in markets:
        if counts[m.source] >= per_source:
            continue
        counts[m.source] += 1
        try:
            series, payload = fetch_history(m, http)
            result[m.key] = series
            raw.append(payload)
        except (APIError, KeyError, ValueError, TypeError) as exc:
            errors.append({"market_id": m.key, "error": type(exc).__name__})
    return result, raw, errors


def features(series: NativeHistory, m: Market, as_of: str) -> dict:
    if series.key != m.key:
        raise ValueError("History does not belong to market")
    if parse_time(series.received_at) > parse_time(as_of):
        return {"e_native_history": {"available": False, "reason": "received_after_analysis"}}
    # The series can be fetched after m.observed_at, but only earlier event times
    # enter the evidence. The current Gamma price is never mixed into CLOB deltas.
    points = [p for p in series.points if parse_time(p.event_time) <= parse_time(m.observed_at)]
    original_count = len(points)
    if series.source == "polymarket":
        # The endpoint can append a partial latest point. Select actual samples
        # just before completed UTC hour boundaries, without interpolation.
        anchors = []
        boundary = parse_time(m.observed_at).replace(minute=0, second=0, microsecond=0)
        for hour in range(49):
            target = boundary - timedelta(hours=48 - hour)
            candidates = [
                p for p in points if 0 <= (target - parse_time(p.event_time)).total_seconds() <= 600
            ]
            if candidates:
                chosen = max(candidates, key=lambda p: parse_time(p.event_time))
                if not anchors or anchors[-1].event_time != chosen.event_time:
                    anchors.append(chosen)
        points = anchors
    summary = {
        "available": bool(points),
        "point_count": len(points),
        "raw_point_count": original_count,
        "basis": series.basis,
        "received_at": series.received_at,
        "endpoint": series.endpoint,
        "issues": series.issues,
        "note": "Native series reconstructed at received_at; historical rule versions "
        "and contemporaneous availability are not established.",
        "sampling": "Actual samples at/before completed UTC hour boundaries, within 10 min; "
        "no interpolation."
        if series.source == "polymarket"
        else "Completed hourly candles.",
    }
    evidence = {"e_native_history": summary}
    if not points:
        return evidence
    latest = points[-1]
    latest_t = parse_time(latest.event_time)
    age = (parse_time(m.observed_at) - latest_t).total_seconds() / 60
    summary.update(latest_event_time=latest.event_time, latest_age_minutes=round(age, 3))
    if age > 90:
        summary.update(available=False, reason="latest_native_point_older_than_90_minutes")
        return evidence
    for hours, tolerance in [(1, 0.25), (24, 2)]:
        candidates = [
            p
            for p in points
            if abs((latest_t - parse_time(p.event_time)).total_seconds() / 3600 - hours)
            <= tolerance
        ]
        if not candidates:
            continue
        previous = min(
            candidates,
            key=lambda p: abs((latest_t - parse_time(p.event_time)).total_seconds() / 3600 - hours),
        )
        evidence[f"e_change_{hours}h"] = {
            "value": round(latest.probability - previous.probability, 8),
            "unit": "probability",
            "origin": "exchange_native_history",
            "basis": series.basis,
            "elapsed_hours": round(
                (latest_t - parse_time(previous.event_time)).total_seconds() / 3600, 4
            ),
            "baseline_observed_at": previous.event_time,
            "baseline_probability": previous.probability,
            "current_event_time": latest.event_time,
            "current_probability": latest.probability,
        }
    moves = []
    for a, b in zip(points, points[1:]):
        elapsed = (parse_time(b.event_time) - parse_time(a.event_time)).total_seconds() / 3600
        if 0.5 <= elapsed <= 1.5:
            moves.append((b.event_time, (b.probability - a.probability) / elapsed))
    if len(moves) >= 9 and moves[-1][0] == latest.event_time:
        past = [rate for _, rate in moves[:-1]]
        center = statistics.median(past)
        mad = statistics.median(abs(rate - center) for rate in past)
        z = (moves[-1][1] - center) / max(1.4826 * mad, 0.005)
        evidence["e_robust_z"] = {
            "value": round(z, 4),
            "baseline_moves": len(past),
            "median_rate": center,
            "mad": mad,
            "scale_floor": 0.005,
            "unit": "robust_standardized_hourly_move",
            "origin": "exchange_native_history",
            "basis": series.basis,
            "current_event_time": latest.event_time,
        }
    return evidence
