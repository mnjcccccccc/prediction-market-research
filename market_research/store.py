"""SQLite snapshot history; reads are always bounded by the analysis timestamp."""

import json
from pathlib import Path
import sqlite3

from .models import Market, parse_time
from .native_history import NativeHistory


class Store:
    def __init__(self, path: str | Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute("""CREATE TABLE IF NOT EXISTS snapshots (
            source TEXT NOT NULL, market_id TEXT NOT NULL, ts REAL NOT NULL,
            payload TEXT NOT NULL, PRIMARY KEY (source, market_id, ts))""")
        self.db.execute("""CREATE TABLE IF NOT EXISTS native_history (
            source TEXT NOT NULL, market_id TEXT NOT NULL, received_ts REAL NOT NULL,
            payload TEXT NOT NULL, PRIMARY KEY (source, market_id, received_ts))""")

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def save(self, markets: list[Market]):
        with self.db:
            self.db.executemany(
                "INSERT OR IGNORE INTO snapshots VALUES (?,?,?,?)",
                [
                    (
                        m.source,
                        m.market_id,
                        parse_time(m.observed_at).timestamp(),
                        json.dumps(m.to_dict(), ensure_ascii=False, allow_nan=False),
                    )
                    for m in markets
                ],
            )

    def history(self, market: Market, hours: float = 48) -> list[Market]:
        end = parse_time(market.observed_at).timestamp()
        rows = self.db.execute(
            "SELECT payload FROM snapshots WHERE source=? AND market_id=? "
            "AND ts>=? AND ts<=? ORDER BY ts",
            (market.source, market.market_id, end - hours * 3600, end),
        )
        return [Market.from_dict(json.loads(row[0])) for row in rows]

    def save_native(self, series: list[NativeHistory]):
        with self.db:
            self.db.executemany(
                "INSERT OR IGNORE INTO native_history VALUES (?,?,?,?)",
                [
                    (
                        h.source,
                        h.market_id,
                        parse_time(h.received_at).timestamp(),
                        json.dumps(h.to_dict(), ensure_ascii=False, allow_nan=False),
                    )
                    for h in series
                ],
            )

    def native_for(self, market: Market, as_of: str) -> NativeHistory | None:
        row = self.db.execute(
            "SELECT payload FROM native_history WHERE source=? AND market_id=? "
            "AND received_ts<=? ORDER BY received_ts DESC LIMIT 1",
            (market.source, market.market_id, parse_time(as_of).timestamp()),
        ).fetchone()
        return NativeHistory.from_dict(json.loads(row[0])) if row else None

    def latest(self, as_of: str | None = None) -> list[Market]:
        end = parse_time(as_of).timestamp() if as_of else 1e20
        rows = self.db.execute(
            """SELECT s.payload FROM snapshots s JOIN
            (SELECT source,market_id,MAX(ts) ts FROM snapshots WHERE ts<=?
             GROUP BY source,market_id) t
            ON s.source=t.source AND s.market_id=t.market_id AND s.ts=t.ts
            ORDER BY s.source,s.market_id""",
            (end,),
        )
        return [Market.from_dict(json.loads(row[0])) for row in rows]
