"""
core/decision_engine.py

DecisionEngine

Evaluate whether a trade action should be allowed, based on inputs from the
confidence engine, multi-timeframe analyzer, institutional filter, current
positions, news/session status, spread and risk settings.

Returns a small decision dict:
{
    "action": "BUY" | "SELL" | "WAIT",
    "confidence": int,   # rounded 0..100
    "reason": str,       # human-readable single-line reason
    "allow_trade": bool  # True only when action is BUY/SELL and all checks pass
}

Rules enforced (production-safety oriented):
- Never BUY if higher timeframes (H4 or H1) are BEARISH.
- Never SELL if higher timeframes (H4 or H1) are BULLISH.
- Never trade during high-impact news.
- Never trade outside allowed sessions.
- Never trade if spread exceeds configured limit.
- Never open duplicate trades on the same symbol.
- Minimum confidence threshold (default 75).
- If any rule fails -> action is "WAIT" and allow_trade is False.

The engine is defensive about input shapes (accepts dicts and objects for positions)
and logs decisions at INFO/DEBUG level for traceability.

Author: production-ready implementation for JarvisOS
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional, Sequence, Union

logger = logging.getLogger("DecisionEngine")
if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"))
    logger.addHandler(ch)
logger.setLevel(logging.INFO)


class DecisionEngine:
    """
    DecisionEngine encapsulates the trading rules that determine whether
    an automated or semi-automated trade should proceed.
    """

    def __init__(self, min_confidence: float = 75.0, default_max_spread: float = 3.0):
        """
        :param min_confidence: minimal required confidence (0-100) to allow a trade
        :param default_max_spread: default maximum allowed spread (in pips/points) if not supplied in risk_settings
        """
        self.min_confidence = float(min_confidence)
        self.default_max_spread = float(default_max_spread)
        logger.info("DecisionEngine initialized min_confidence=%s default_max_spread=%s", self.min_confidence, self.default_max_spread)

    # Public API
    def decide(
        self,
        confidence_result: Dict[str, Any],
        multi_timeframe: Optional[Dict[str, Any]],
        institutional: Optional[Dict[str, Any]],
        open_positions: Optional[Sequence[Any]],
        news_high_impact: bool,
        session_allowed: bool,
        spread: float,
        risk_settings: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Union[str, int, bool]]:
        """
        Make a trade decision.

        :param confidence_result: output of ConfidenceEngine.evaluate()
               expected keys: "signal" (BUY/SELL/WAIT), "confidence" (0..100), optionally "reasons"
        :param multi_timeframe: output of MultiTimeframe.analyze()
               expected to include timeframes dict with H4 and H1 trends and "overall"
        :param institutional: output of InstitutionalFilter.analyze() (kept for completeness)
        :param open_positions: sequence of open position objects or dicts (each should expose a symbol)
        :param news_high_impact: True if high-impact news is active
        :param session_allowed: True if trading session is allowed
        :param spread: current spread (in pips/points). Caller is responsible for units consistency with risk_settings.
        :param risk_settings: dict containing optional keys:
               - "max_spread": float
               - "symbol": str
               - "allow_duplicate": bool (default False)
        :returns: dict with keys action, confidence, reason, allow_trade
        """
        # Defensive defaults
        risk_settings = risk_settings or {}
        symbol = risk_settings.get("symbol") or self._infer_symbol_from_sources(confidence_result, multi_timeframe, institutional)
        max_spread = float(risk_settings.get("max_spread", self.default_max_spread))
        allow_duplicate = bool(risk_settings.get("allow_duplicate", False))

        # Extract confidence and intended action
        try:
            action = str(confidence_result.get("signal", "WAIT")).upper()
        except Exception:
            action = "WAIT"

        try:
            confidence_val = float(confidence_result.get("confidence", 0.0))
        except Exception:
            confidence_val = 0.0

        confidence_int = int(round(max(0.0, min(100.0, confidence_val))))

        logger.info("Decision request: symbol=%s action=%s confidence=%s spread=%s session_allowed=%s news_high_impact=%s",
                    symbol, action, confidence_int, spread, session_allowed, news_high_impact)

        # Initialize decision result with conservative defaults
        result = {
            "action": "WAIT",
            "confidence": confidence_int,
            "reason": "Default: no action",
            "allow_trade": False
        }

        # If advised action is WAIT, respect it
        if action not in ("BUY", "SELL"):
            logger.info("ConfidenceEngine advised WAIT or unsupported action (%s). No trade.", action)
            result.update({"action": "WAIT", "reason": "Signal is WAIT or unknown", "allow_trade": False})
            return result

        # Rule 1: Never trade during high-impact news
        if news_high_impact:
            reason = "Blocked: High-impact news active"
            logger.info(reason)
            return self._blocked(action, confidence_int, reason)

        # Rule 2: Never trade outside allowed session
        if not session_allowed:
            reason = "Blocked: Trading not allowed in current session"
            logger.info(reason)
            return self._blocked(action, confidence_int, reason)

        # Rule 3: Never trade if spread exceeds limit
        if spread is None:
            logger.warning("Spread value missing; blocking trade for safety")
            return self._blocked(action, confidence_int, "Blocked: Spread unknown")
        try:
            if float(spread) > float(max_spread):
                reason = f"Blocked: Spread {spread} exceeds max allowed {max_spread}"
                logger.info(reason)
                return self._blocked(action, confidence_int, reason)
        except Exception:
            logger.exception("Error comparing spread; blocking trade for safety")
            return self._blocked(action, confidence_int, "Blocked: Spread check failed")

        # Rule 4: Never open duplicate trades (same symbol) unless explicitly allowed
        if not allow_duplicate:
            if symbol is None:
                # Conservative behavior: if symbol cannot be determined, block trade to avoid duplicates
                reason = "Blocked: Symbol unknown (cannot enforce duplicate trade protection)"
                logger.warning(reason)
                return self._blocked(action, confidence_int, reason)
            if self._has_open_position_on_symbol(open_positions, symbol):
                reason = f"Blocked: Existing open position detected for {symbol}"
                logger.info(reason)
                return self._blocked(action, confidence_int, reason)

        # Rule 5: Higher timeframe checks
        # Obtain H4 and H1 trends if available
        h4_trend = self._get_mtf_trend(multi_timeframe, "H4")
        h1_trend = self._get_mtf_trend(multi_timeframe, "H1")
        logger.debug("Higher timeframe trends: H4=%s H1=%s", h4_trend, h1_trend)

        if action == "BUY":
            # Never BUY if higher timeframes are bearish (H4 or H1)
            if h4_trend == "BEARISH" or h1_trend == "BEARISH":
                reason = "Blocked: Higher timeframe(s) bearish"
                logger.info(reason)
                return self._blocked(action, confidence_int, reason)
        elif action == "SELL":
            # Never SELL if higher timeframes are bullish
            if h4_trend == "BULLISH" or h1_trend == "BULLISH":
                reason = "Blocked: Higher timeframe(s) bullish"
                logger.info(reason)
                return self._blocked(action, confidence_int, reason)

        # Rule 6: Minimum confidence threshold
        if confidence_int < int(round(self.min_confidence)):
            reason = f"Blocked: Confidence {confidence_int} below minimum required {int(round(self.min_confidence))}"
            logger.info(reason)
            return self._blocked(action, confidence_int, reason)

        # All checks passed: allow trade
        reason = "Approved: All checks passed"
        logger.info("%s allowed for %s (confidence=%s)", action, symbol or "<unknown symbol>", confidence_int)
        result.update({"action": action, "confidence": confidence_int, "reason": reason, "allow_trade": True})
        return result

    # -------------------------
    # Helper utilities
    # -------------------------
    def _blocked(self, action: str, confidence: int, reason: str) -> Dict[str, Union[str, int, bool]]:
        """
        Helper to return a standardized blocked result.
        """
        return {"action": "WAIT", "confidence": confidence, "reason": reason, "allow_trade": False}

    def _get_mtf_trend(self, mtf_result: Optional[Dict[str, Any]], timeframe: str) -> Optional[str]:
        """
        Safely extract the trend string for a given timeframe name from a MultiTimeframe result.
        Returns None when unavailable.
        """
        try:
            if not mtf_result or not isinstance(mtf_result, dict):
                return None
            tfs = mtf_result.get("timeframes")
            if not tfs or not isinstance(tfs, dict):
                return None
            info = tfs.get(timeframe)
            if not info or not isinstance(info, dict):
                return None
            trend = info.get("trend")
            if isinstance(trend, str):
                return trend.upper()
            return None
        except Exception:
            logger.exception("Error extracting %s trend from multi_timeframe", timeframe)
            return None

    def _has_open_position_on_symbol(self, positions: Optional[Sequence[Any]], symbol: Optional[str]) -> bool:
        """
        Determine whether there is an open position for the provided symbol.
        Positions may be sequence of objects exposing `.symbol` or mapping with 'symbol' key.
        Returns True if any position matches the symbol (case-insensitive).
        """
        if symbol is None:
            logger.debug("_has_open_position_on_symbol: symbol is None -> cannot check duplicates")
            return False  # caller should decide conservatively; we return False to continue logic

        if not positions:
            return False

        symbol_norm = symbol.strip().upper()
        for pos in positions:
            try:
                pos_symbol = None
                if isinstance(pos, dict):
                    pos_symbol = pos.get("symbol") or pos.get("instrument")
                else:
                    # object attribute
                    pos_symbol = getattr(pos, "symbol", None) or getattr(pos, "instrument", None)
                if pos_symbol and str(pos_symbol).strip().upper() == symbol_norm:
                    logger.debug("Found existing position for symbol %s", symbol_norm)
                    return True
            except Exception:
                logger.exception("Error reading position symbol; skipping position in duplicate check")
                continue
        return False

    def _infer_symbol_from_sources(self, *sources: Dict[str, Any]) -> Optional[str]:
        """
        Try to infer symbol from provided sources (confidence_result, multi_timeframe, institutional, ...).
        Returns first non-empty symbol found (uppercased) or None.
        """
        for src in sources:
            if not src or not isinstance(src, dict):
                continue
            # Common keys that might contain symbol
            for key in ("symbol", "instrument", "ticker"):
                val = src.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip().upper()
        return None
