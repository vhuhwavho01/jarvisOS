"""
core/money_manager.py

MoneyManager - position sizing and money management utilities.

- Uses TradeManager.calculate_lot_size when available for consistency with live trading.
- Provides risk-percent sizing and dynamic lot calculation helpers.
- Includes conservative fallback calculations and simple Kelly utility.
- Production-ready: logging, type hints, docstrings, defensive coding.
"""

from __future__ import annotations

import logging
from typing import Optional

from core.trade_manager import TradeManager

logger = logging.getLogger("MoneyManager")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)


class MoneyManager:
    """
    MoneyManager handles position sizing logic.

    Typical usage:
        mm = MoneyManager(trade_manager=TradeManager())
        lot = mm.lot_from_risk_percent(balance=10000, risk_percent=1.0, stop_loss_points=50)
    """

    def __init__(self, trade_manager: Optional[TradeManager] = None):
        """
        :param trade_manager: Optional TradeManager instance. If provided, its calculate_lot_size method
                              will be used as the primary sizing engine for consistency with broker behavior.
        """
        self.trade_manager = trade_manager
        logger.info("MoneyManager initialized (trade_manager=%s)", type(trade_manager).__name__ if trade_manager else "None")

    def lot_from_risk_percent(
        self,
        balance: float,
        risk_percent: float,
        stop_loss_points: float,
        pip_value: float = 10.0,
        min_lot: float = 0.01,
        max_lot: Optional[float] = None,
    ) -> float:
        """
        Compute lot size that risks `risk_percent` percent of the balance for the given stop loss (in points).

        Steps:
          - Prefer using TradeManager.calculate_lot_size if available.
          - Otherwise fall back to a conservative calculation:
                lot = (balance * risk_percent/100) / (stop_loss_points * pip_value)

        The result is clamped to [min_lot, max_lot] when provided.

        :param balance: account balance in account currency
        :param risk_percent: percent of balance to risk (e.g., 1.0 for 1%)
        :param stop_loss_points: stop-loss distance in points/pips (must be > 0)
        :param pip_value: per-pip monetary value for the instrument at 1 lot (default 10)
        :param min_lot: minimum allowed lot size (default 0.01)
        :param max_lot: optional maximum lot size cap
        :return: lot size rounded to 2 decimal places
        """
        try:
            if stop_loss_points <= 0:
                logger.warning("stop_loss_points <= 0, returning min_lot=%s", min_lot)
                return float(min_lot)

            # Use TradeManager if present for consistent broker-aware computation
            if self.trade_manager is not None and hasattr(self.trade_manager, "calculate_lot_size"):
                try:
                    lot = float(self.trade_manager.calculate_lot_size(balance, risk_percent, stop_loss_points, pip_value))
                    logger.debug("Lot calculated via TradeManager: %s", lot)
                except Exception:
                    logger.exception("TradeManager.calculate_lot_size failed; falling back to internal calc")
                    lot = self._fallback_lot_calc(balance, risk_percent, stop_loss_points, pip_value)
            else:
                lot = self._fallback_lot_calc(balance, risk_percent, stop_loss_points, pip_value)

            # enforce bounds
            lot = max(float(min_lot), lot)
            if max_lot is not None:
                lot = min(float(max_lot), lot)

            # round to sensible increment
            lot = round(lot, 2)
            logger.info("Computed lot size: %s (balance=%s risk=%s sl_points=%s)", lot, balance, risk_percent, stop_loss_points)
            return lot
        except Exception:
            logger.exception("Unexpected error computing lot; returning min_lot")
            return float(min_lot)

    def _fallback_lot_calc(self, balance: float, risk_percent: float, stop_loss_points: float, pip_value: float) -> float:
        """
        Simple fallback lot calculation.
        """
        try:
            risk_amount = float(balance) * (float(risk_percent) / 100.0)
            lot = risk_amount / (float(stop_loss_points) * float(pip_value))
            lot = max(0.01, lot)
            return lot
        except Exception:
            logger.exception("Fallback lot calc error")
            return 0.01

    def kelly_fraction(self, win_rate: float, win_loss_ratio: float) -> float:
        """
        Rough Kelly criterion fraction (not recommended to use full Kelly).
        k = (win_rate - (1 - win_rate)/win_loss_ratio)
        Returns fraction (0..1). Caller should scale down (e.g., 0.25 * k) for safety.

        :param win_rate: fraction (0..1)
        :param win_loss_ratio: avg_win / avg_loss (positive number)
        """
        try:
            w = float(win_rate)
            r = float(win_loss_ratio)
            if r <= 0:
                return 0.0
            k = (w - (1.0 - w) / r)
            # clamp sensible range
            k = max(0.0, min(1.0, k))
            return k
        except Exception:
            logger.exception("Kelly calculation error")
            return 0.0
