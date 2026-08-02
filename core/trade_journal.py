"""
core/trade_journal.py

TradeJournal - persistent trade logging layer with asynchronous writes and MT5 deal watcher.

Features:
- SQLite-backed persistent journal for trades.
- Non-blocking async writer queue: use record_order_async(request, result) to enqueue order attempts.
- Synchronous record_trade(...) kept for deterministic backtest writes.
- Background deal watcher that polls mt5.history_deals_get and updates journal rows with realized P/L when deals complete.
- In-memory maps (order_id -> rowid, deal_id -> rowid) to efficiently reconcile deals to journal rows.
- Thread-safe and defensive against failures.

Schema:
- trades(id INTEGER PRIMARY KEY AUTOINCREMENT,
         timestamp TEXT,
         symbol TEXT,
         side TEXT,
         volume REAL,
         price REAL,
         sl REAL,
         tp REAL,
         pnl REAL,
         comment TEXT,
         meta TEXT)

Notes:
- The deal watcher uses a polling approach (MT5 Python API has no direct callback mechanism available in all environments).
- Start the deal watcher by calling start_deal_watcher(); stop with stop_deal_watcher().
"""

from __future__ import annotations

import json
import logging
import os
import queue
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import MetaTrader5 as mt5

logger = logging.getLogger("TradeJournal")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)

DEFAULT_DB_NAME = "trade_journal.db"


class TradeJournal:
    """
    SQLite-backed trade journal with async writer and MT5 deal reconciliation.

    Usage:
      journal = TradeJournal(db_path="data/trade_journal.db")
      journal.record_order_async(request, result)   # called by TradeManager for live orders
      journal.start_deal_watcher()                  # start background deal reconciliation
      journal.stop_deal_watcher()                   # stop it on shutdown
      journal.record_trade(...)                     # synchronous insert used by backtester
    """

    def __init__(self, db_path: Optional[str] = None, start_writer: bool = True):
        self.db_path = db_path or os.path.join(os.getcwd(), DEFAULT_DB_NAME)
        # ensure directory
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        self._conn: sqlite3.Connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.RLock()

        self._create_schema()

        # Async writer queue and thread
        self._write_queue: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._writer_thread: Optional[threading.Thread] = None
        self._writer_stop = threading.Event()
        if start_writer:
            self._start_writer_thread()

        # Maps to quickly reconcile incoming MT5 deals with journal rows
        self._order_map: Dict[int, int] = {}  # order_id -> journal_rowid
        self._deal_map: Dict[int, int] = {}   # deal_id -> journal_rowid
        self._map_lock = threading.RLock()

        # Deal watcher thread
        self._deal_thread: Optional[threading.Thread] = None
        self._deal_stop = threading.Event()
        self._last_deal_check_time = datetime.utcnow() - timedelta(minutes=10)

        logger.info("TradeJournal initialized at %s", self.db_path)

    # ---------------------------
    # DB schema
    # ---------------------------
    def _create_schema(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    symbol TEXT NOT NULL,
                    side TEXT NOT NULL,
                    volume REAL NOT NULL,
                    price REAL NOT NULL,
                    sl REAL,
                    tp REAL,
                    pnl REAL,
                    comment TEXT,
                    meta TEXT
                )
                """
            )
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_symbol ON trades(symbol)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_timestamp ON trades(timestamp)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_trades_meta ON trades(meta)")
            self._conn.commit()

    # ---------------------------
    # Synchronous record (backtester / guaranteed)
    # ---------------------------
    def record_trade(
        self,
        symbol: str,
        side: str,
        volume: float,
        price: float,
        sl: Optional[float] = None,
        tp: Optional[float] = None,
        pnl: Optional[float] = None,
        comment: Optional[str] = None,
        meta: Optional[str] = None,
        timestamp: Optional[datetime] = None,
    ) -> int:
        """
        Synchronously insert a trade record and return row id.
        Intended to be used by backtester (deterministic).
        """
        timestamp = timestamp or datetime.utcnow()
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                INSERT INTO trades(timestamp, symbol, side, volume, price, sl, tp, pnl, comment, meta)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (timestamp.isoformat(), symbol, side, volume, price, sl, tp, pnl, comment, meta),
            )
            self._conn.commit()
            rowid = cur.lastrowid
            logger.debug("Synchronous trade recorded id=%s %s %s @%s vol=%s pnl=%s", rowid, symbol, side, price, volume, pnl)
            return rowid

    # ---------------------------
    # Async writer
    # ---------------------------
    def _start_writer_thread(self) -> None:
        with self._lock:
            if self._writer_thread and self._writer_thread.is_alive():
                return
            self._writer_stop.clear()
            self._writer_thread = threading.Thread(target=self._writer_loop, daemon=True, name="TradeJournalWriter")
            self._writer_thread.start()
            logger.info("TradeJournal async writer started")

    def _stop_writer_thread(self, join: bool = True, timeout: float = 5.0) -> None:
        self._writer_stop.set()
        if self._writer_thread and join:
            self._writer_thread.join(timeout=timeout)
            logger.info("TradeJournal async writer stopped")

    def _writer_loop(self) -> None:
        while not self._writer_stop.is_set():
            try:
                item = None
                try:
                    item = self._write_queue.get(timeout=0.5)
                except queue.Empty:
                    continue
                if item is None:
                    continue
                try:
                    self._write_order_item(item)
                except Exception:
                    logger.exception("Failed to write queued order item")
                finally:
                    self._write_queue.task_done()
            except Exception:
                logger.exception("Unexpected error in TradeJournal writer loop")
        # flush remaining items
        while True:
            try:
                item = self._write_queue.get_nowait()
            except queue.Empty:
                break
            try:
                self._write_order_item(item)
            except Exception:
                logger.exception("Error flushing journal writer")
            finally:
                self._write_queue.task_done()

    def record_order_async(self, request: Dict[str, Any], result: Any) -> None:
        """
        Enqueue an order attempt for asynchronous journaling.
        This is the non-blocking API intended for live trading usage.
        """
        try:
            payload = {"timestamp": datetime.utcnow().isoformat(), "request": request, "result": self._safe_serialize_result(result)}
            self._write_queue.put(payload)
        except Exception:
            logger.exception("Failed to enqueue order for journaling")

    def _safe_serialize_result(self, result: Any) -> Dict[str, Any]:
        """
        Convert MT5 result object or dict into JSON-friendly dict (best-effort).
        """
        try:
            if result is None:
                return {"_raw": None}
            if isinstance(result, dict):
                # ensure serializable
                return {k: (v if isinstance(v, (str, int, float, bool, type(None))) else str(v)) for k, v in result.items()}
            # attempt to extract attributes
            out: Dict[str, Any] = {}
            for attr in dir(result):
                if attr.startswith("_"):
                    continue
                try:
                    val = getattr(result, attr)
                    if callable(val):
                        continue
                    out[attr] = val if isinstance(val, (str, int, float, bool, type(None))) else str(val)
                except Exception:
                    continue
            return out
        except Exception:
            try:
                return {"_repr": repr(result)}
            except Exception:
                return {"_error": "serialization_failed"}

    def _write_order_item(self, item: Dict[str, Any]) -> None:
        """
        Convert a queued item into an actual DB row and update maps for order/deal reconciliation.
        """
        try:
            req = item.get("request", {})
            res = item.get("result", {})
            ts = item.get("timestamp") or datetime.utcnow().isoformat()
            symbol = req.get("symbol", "UNKNOWN")
            raw_type = req.get("type")
            side = "UNKNOWN"

            # determine side (clean, no stray diff markers)
            if raw_type == mt5.ORDER_TYPE_BUY:
                side = "BUY"
            elif raw_type == mt5.ORDER_TYPE_SELL:
                side = "SELL"
            else:
                # fallback use comment/action
                side = req.get("comment", "") or str(req.get("action", "DEAL"))

            volume = float(req.get("volume", 0.0) or 0.0)
            price = res.get("price") if isinstance(res, dict) else None
            if price is None:
                price = req.get("price", 0.0)
            sl = req.get("sl")
            tp = req.get("tp")
            comment = req.get("comment") or (res.get("comment") if isinstance(res, dict) else "")
            pnl = None
            meta_json = None
            try:
                meta_json = json.dumps({"request": req, "result": res}, default=str)
            except Exception:
                meta_json = repr({"request": req, "result": res})

            rowid = self.record_trade(
                symbol=str(symbol),
                side=str(side),
                volume=float(volume),
                price=float(price) if price is not None else 0.0,
                sl=(float(sl) if sl is not None else None),
                tp=(float(tp) if tp is not None else None),
                pnl=pnl,
                comment=str(comment),
                meta=meta_json,
                timestamp=datetime.fromisoformat(ts),
            )

            # If result contains order/deal ids, map them to this row for later reconciliation
            try:
                if isinstance(res, dict):
                    order_id = res.get("order")
                    deal_id = res.get("deal")
                    # For some MT5 wrappers retcode may be present but not 'order', adapt to possible keys
                    with self._map_lock:
                        if order_id is not None:
                            try:
                                self._order_map[int(order_id)] = rowid
                            except Exception:
                                pass
                        if deal_id is not None:
                            try:
                                self._deal_map[int(deal_id)] = rowid
                            except Exception:
                                pass
            except Exception:
                logger.exception("Error mapping order/deal ids for rowid=%s", rowid)

            # If the result already contains a realized profit, update the record now
            try:
                profit = None
                if isinstance(res, dict):
                    # some wrappers include 'profit' directly
                    profit = res.get("profit")
                if profit is not None:
                    self._update_row_pnl(rowid, float(profit), extra_comment="(initial result provided profit)")
            except Exception:
                logger.debug("No immediate profit to update for row %s", rowid)

            logger.debug("Async journal write complete rowid=%s symbol=%s side=%s", rowid, symbol, side)
        except Exception:
            logger.exception("Failed to write order item to DB")

    # ---------------------------
    # Deal watcher to reconcile realized P/L
    # ---------------------------
    def start_deal_watcher(self, poll_interval: float = 2.0) -> None:
        """
        Start background thread that polls MT5 deal history and updates journal entries with realized P/L.
        """
        with self._map_lock:
            if self._deal_thread and self._deal_thread.is_alive():
                logger.debug("Deal watcher already running")
                return
            self._deal_stop.clear()
            self._deal_thread = threading.Thread(target=self._deal_watch_loop, args=(poll_interval,), daemon=True, name="TradeJournalDealWatcher")
            self._deal_thread.start()
            logger.info("TradeJournal deal watcher started (poll_interval=%ss)", poll_interval)

    def stop_deal_watcher(self, join: bool = True, timeout: float = 5.0) -> None:
        self._deal_stop.set()
        if self._deal_thread and join:
            self._deal_thread.join(timeout=timeout)
            logger.info("TradeJournal deal watcher stopped")

    def _deal_watch_loop(self, poll_interval: float) -> None:
        """
        Poll history_deals_get for new deals. For each deal, attempt to update the journal row
        that corresponds to the order or deal id. If no mapping exists, optionally insert a new row.
        """
        logger.debug("Deal watcher loop started")
        while not self._deal_stop.is_set():
            try:
                start = self._last_deal_check_time
                end = datetime.utcnow() + timedelta(seconds=1)
                deals = mt5.history_deals_get(start, end)
                if deals:
                    for d in deals:
                        try:
                            # Extract deal attributes (best-effort)
                            deal_id = getattr(d, "deal", None) or (d.get("deal") if isinstance(d, dict) else None)
                            order_id = getattr(d, "order", None) or (d.get("order") if isinstance(d, dict) else None)
                            symbol = getattr(d, "symbol", None) or (d.get("symbol") if isinstance(d, dict) else "UNKNOWN")
                            profit = getattr(d, "profit", None) or (d.get("profit") if isinstance(d, dict) else None)
                            volume = getattr(d, "volume", None) or (d.get("volume") if isinstance(d, dict) else None)
                            price = getattr(d, "price", None) or (d.get("price") if isinstance(d, dict) else None)
                            # try find by deal or order map
                            rowid = None
                            with self._map_lock:
                                if deal_id is not None and int(deal_id) in self._deal_map:
                                    rowid = self._deal_map[int(deal_id)]
                                elif order_id is not None and int(order_id) in self._order_map:
                                    rowid = self._order_map[int(order_id)]
                            if rowid:
                                # update pnl for row
                                try:
                                    if profit is not None:
                                        self._update_row_pnl(rowid, float(profit), extra_comment=f"(deal {deal_id} reconciled)")
                                        # map the deal id as well to row
                                        with self._map_lock:
                                            if deal_id is not None:
                                                self._deal_map[int(deal_id)] = rowid
                                except Exception:
                                    logger.exception("Failed to update journal row %s for deal %s", rowid, deal_id)
                            else:
                                # No mapping found; create a new journal entry for this deal (best-effort)
                                try:
                                    # infer side from profit & volume sign if available - we set side UNKNOWN otherwise
                                    side = "UNKNOWN"
                                    # write a separate row to record this deal
                                    meta = json.dumps({"deal": _safe_to_dict(d)}, default=str)
                                    self.record_trade(
                                        symbol=str(symbol),
                                        side=side,
                                        volume=float(volume) if volume is not None else 0.0,
                                        price=float(price) if price is not None else 0.0,
                                        sl=None,
                                        tp=None,
                                        pnl=float(profit) if profit is not None else None,
                                        comment=f"reconciled_deal_{deal_id}",
                                        meta=meta,
                                        timestamp=datetime.utcfromtimestamp(getattr(d, "time", time.time()) if hasattr(d, "time") else (d.get("time") if isinstance(d, dict) else time.time())),
                                    )
                                except Exception:
                                    logger.exception("Failed to insert journal row for unmatched deal %s", deal_id)
                        except Exception:
                            logger.exception("Error processing deal item from mt5")
                # update last check time
                self._last_deal_check_time = end
            except Exception:
                logger.exception("Error in deal watcher loop")
            # wait with early exit
            if self._deal_stop.wait(poll_interval):
                break
        logger.debug("Deal watcher loop exiting")

    def _update_row_pnl(self, rowid: int, pnl: float, extra_comment: Optional[str] = None) -> None:
        """
        Update the pnl and comment for an existing journal row.
        """
        try:
            with self._lock:
                cur = self._conn.cursor()
                # Fetch existing comment to append
                cur.execute("SELECT comment FROM trades WHERE id = ?", (rowid,))
                row = cur.fetchone()
                existing_comment = row["comment"] if row and "comment" in row.keys() else ""
                new_comment = existing_comment or ""
                if extra_comment:
                    if new_comment:
                        new_comment = f"{new_comment} | {extra_comment}"
                    else:
                        new_comment = extra_comment
                cur.execute("UPDATE trades SET pnl = ?, comment = ? WHERE id = ?", (pnl, new_comment, rowid))
                self._conn.commit()
                logger.info("Updated journal row %s with pnl=%s", rowid, pnl)
        except Exception:
            logger.exception("Failed to update journal row %s", rowid)

    # ---------------------------
    # Utilities
    # ---------------------------
    def fetch_trades(self, limit: Optional[int] = None, symbol: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._lock:
            cur = self._conn.cursor()
            if symbol:
                sql = "SELECT * FROM trades WHERE symbol = ? ORDER BY timestamp ASC"
                params = (symbol,)
            else:
                sql = "SELECT * FROM trades ORDER BY timestamp ASC"
                params = ()
            if limit:
                sql += " LIMIT ?"
                params = params + (limit,)
            cur.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
            return rows

    def export_csv(self, file_path: str) -> None:
        import csv

        trades = self.fetch_trades()
        if not trades:
            logger.info("No trades to export")
            return
        keys = list(trades[0].keys())
        with open(file_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=keys)
            writer.writeheader()
            for t in trades:
                writer.writerow(t)
        logger.info("Exported %s trades to %s", len(trades), file_path)

    def close(self) -> None:
        """
        Stop background threads and close DB connection.
        """
        try:
            self._stop_writer_thread()
            self.stop_deal_watcher()
            with self._lock:
                if self._conn:
                    self._conn.close()
                    self._conn = None  # type: ignore
                    logger.info("TradeJournal closed")
        except Exception:
            logger.exception("Error closing TradeJournal")


def _safe_to_dict(obj: Any) -> Dict[str, Any]:
    """
    Helper to convert a deal object or dict to a plain mapping.
    """
    try:
        if isinstance(obj, dict):
            return obj
        result = {}
        for attr in dir(obj):
            if attr.startswith("_"):
                continue
            try:
                val = getattr(obj, attr)
                if callable(val):
                    continue
                result[attr] = val
            except Exception:
                continue
        return result
    except Exception:
        try:
            return {"repr": repr(obj)}
        except Exception:
            return {"error": "cannot_serialize"}
