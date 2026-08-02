"""
core/partial_close_manager.py

PartialCloseManager - logic to perform partial closes under configurable rules.

- Uses MetaTrader5 (mt5) to place an opposite-side deal that reduces a position's volume.
- Performs idempotent partial-close (no repeated closes if position already partially closed) when configured.
- Configurable:
    - profit_threshold_pips: profit in pips required to trigger partial close
    - partial_percent: percent of current position to close (0-100)
    - one_shot: if True, perform only a single partial close per ticket (in-memory tracking)
- Respects instrument minimum volume and volume step (best-effort).
- Emits logs for every decision and action.

Note:
- This manager uses mt5.order_send(...) with the "position" and "volume" fields to request a partial close.
  That matches the way many MT5 bridges accept partial-close requests, but ensure your MT5 connector
  supports partial volume closing via the 'position' argument (standard MetaTrader5 API does).

Usage:
    pcm = PartialCloseManager(trade_manager=trade_manager)
    pcm.apply(position)   # called from a position monitor
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import MetaTrader5 as mt5

logger = logging.getLogger("PartialCloseManager")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)


class PartialCloseManager:
    """
    Manage partial close operations for open positions.

    Parameters:
      trade_manager: Optional TradeManager instance (used to access settings like magic/deviation). If None, defaults are used.
      profit_threshold_pips: Profit in pips required to trigger a partial close.
      partial_percent: Percent of the position to close when triggered (0-100).
      one_shot: If True, perform a single partial close per ticket to avoid repeated reductions.

    Methods:
      apply(position) -> Optional[result]
    """

    def __init__(
        self,
        trade_manager: Optional[Any] = None,
        profit_threshold_pips: float = 30.0,
        partial_percent: float = 50.0,
        one_shot: bool = True,
    ):
        self.trade_manager = trade_manager
        self.profit_threshold_pips = float(profit_threshold_pips)
        self.partial_percent = max(0.0, min(100.0, float(partial_percent)))
        self.one_shot = bool(one_shot)

        # Track tickets we've already partially closed (simple in-memory map)
        self._partial_done: dict[int, bool] = {}

        logger.info(
            "PartialCloseManager initialized threshold=%spips partial_percent=%s one_shot=%s",
            self.profit_threshold_pips,
            self.partial_percent,
            self.one_shot,
        )

    def apply(self, position: Any) -> Optional[Any]:
        """
        Inspect a position and perform a partial close if criteria are met.

        :param position: mt5.Position-like object with attributes: ticket, symbol, type, volume, price_open, sl, tp
        :return: result from mt5.order_send or None if no action was taken
        """
        try:
            ticket = int(getattr(position, "ticket", None))
        except Exception:
            logger.debug("Position missing ticket attribute; skipping partial close")
            return None

        # If one_shot and we've already done a partial close for this ticket, skip
        if self.one_shot and self._partial_done.get(ticket, False):
            logger.debug("Partial close already executed for ticket %s (one_shot mode)", ticket)
            return None

        try:
            symbol = position.symbol
            pos_type = position.type
            entry_price = float(position.price_open)
            current_volume = float(position.volume)
            if current_volume <= 0:
                logger.debug("Position %s volume <= 0; skipping", ticket)
                return None
        except Exception:
            logger.exception("Malformed position object passed to PartialCloseManager")
            return None

        # Fetch symbol info and tick
        s_info = mt5.symbol_info(symbol)
        if s_info is None:
            logger.warning("Symbol info missing for %s; cannot perform partial close", symbol)
            return None

        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            logger.warning("Tick info missing for %s; cannot perform partial close", symbol)
            return None

        point = float(getattr(s_info, "point", 1.0))
        # compute profit in pips
        current_price = float(tick.bid if pos_type == mt5.POSITION_TYPE_BUY else tick.ask)
        profit_in_price = (current_price - entry_price) if pos_type == mt5.POSITION_TYPE_BUY else (entry_price - current_price)
        profit_in_pips = profit_in_price / point

        logger.debug(
            "Evaluating partial close ticket=%s symbol=%s vol=%.2f entry=%s current=%s profit_pips=%.2f",
            ticket,
            symbol,
            current_volume,
            entry_price,
            current_price,
            profit_in_pips,
        )

        # check profit threshold
        if profit_in_pips < self.profit_threshold_pips:
            logger.debug("Ticket %s profit %.2f pips below threshold %.2f -> skip", ticket, profit_in_pips, self.profit_threshold_pips)
            return None

        # compute volume to close
        vol_to_close = round(current_volume * (self.partial_percent / 100.0), 2)
        if vol_to_close <= 0:
            logger.debug("Computed vol_to_close <= 0 for ticket %s -> skip", ticket)
            return None

        # enforce instrument min volume and step (best-effort)
        try:
            min_volume = float(getattr(s_info, "volume_min", 0.01))
            volume_step = float(getattr(s_info, "volume_step", 0.01))
        except Exception:
            min_volume = 0.01
            volume_step = 0.01

        if vol_to_close < min_volume:
            logger.info("Computed partial close volume %.4f < min_volume %.4f; elevating to min_volume", vol_to_close, min_volume)
            vol_to_close = float(min_volume)

        # align to volume_step
        try:
            steps = int(max(1, round(vol_to_close / volume_step)))
            vol_to_close = round(steps * volume_step, 2)
        except Exception:
            vol_to_close = round(vol_to_close, 2)

        # ensure not closing entire position accidentally
        if vol_to_close >= current_volume:
            vol_to_close = round(max(min_volume, current_volume - volume_step), 2)
            if vol_to_close <= 0:
                logger.debug("Adjusted vol_to_close <= 0 after avoiding full close; skip")
                return None

        logger.info("Attempting partial close for ticket=%s symbol=%s vol_to_close=%s", ticket, symbol, vol_to_close)

        # determine opposite order type for partial close
        try:
            if pos_type == mt5.POSITION_TYPE_BUY:
                order_type = mt5.ORDER_TYPE_SELL
                price = float(tick.bid)
            else:
                order_type = mt5.ORDER_TYPE_BUY
                price = float(tick.ask)
        except Exception:
            logger.exception("Error determining order type/price for partial close")
            return None

        # assemble request using 'position' to indicate partial close and desired volume
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "symbol": symbol,
            "volume": float(vol_to_close),
            "type": order_type,
            "price": price,
            "deviation": int(getattr(self.trade_manager, "deviation", 20)) if self.trade_manager is not None else 20,
            "magic": int(getattr(self.trade_manager, "magic", 0)) if self.trade_manager is not None else 0,
            "comment": "JARVIS PARTIAL CLOSE",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        try:
            res = mt5.order_send(request)
            logger.info("Partial close order_send result for ticket=%s: %s", ticket, getattr(res, "__dict__", str(res)))
            # if the order_send appears successful (retcode 0 or TRADE_RETCODE_DONE), mark one-shot
            try:
                retcode = getattr(res, "retcode", None)
                if retcode is None and isinstance(res, dict):
                    retcode = res.get("retcode")
                success = (retcode == 0) or (retcode == getattr(mt5, "TRADE_RETCODE_DONE", 10009))
                if success and self.one_shot:
                    self._partial_done[ticket] = True
            except Exception:
                # even if we can't determine success, mark done to avoid repeat attempts if one_shot
                if self.one_shot:
                    self._partial_done[ticket] = True
            return res
        except Exception:
            logger.exception("mt5.order_send failed for partial close on ticket=%s", ticket)
            return None
