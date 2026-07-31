from core.indicators import Indicators
from core.smart_money import SmartMoney


class StrategyEngine:

    def __init__(self):
        self.smc = SmartMoney()

    def analyze(self, df):

        indicators = Indicators.snapshot(df)
        smc = self.smc.snapshot(df)

        confidence = 0
        reasons = []

        # ==========================================
        # EMA TREND
        # ==========================================

        if indicators["trend"] == "Bullish":
            confidence += 30
            reasons.append("Bullish EMA alignment.")

        elif indicators["trend"] == "Bearish":
            confidence += 30
            reasons.append("Bearish EMA alignment.")

        # ==========================================
        # SMART MONEY TREND
        # ==========================================

        if smc["trend"] == "BULLISH":
            confidence += 30
            reasons.append("Bullish market structure.")

        elif smc["trend"] == "BEARISH":
            confidence += 30
            reasons.append("Bearish market structure.")

        # ==========================================
        # BOS
        # ==========================================

        if smc["bullish_bos"]:
            confidence += 20
            reasons.append("Bullish Break of Structure.")

        if smc["bearish_bos"]:
            confidence += 20
            reasons.append("Bearish Break of Structure.")

        # ==========================================
        # RSI
        # ==========================================

        rsi = float(indicators["rsi"])

        if 45 <= rsi <= 65:
            confidence += 10
            reasons.append("Healthy RSI.")

        elif rsi > 70:
            reasons.append("RSI Overbought.")

        elif rsi < 30:
            reasons.append("RSI Oversold.")

        # ==========================================
        # MACD
        # ==========================================

        if indicators["macd"] > indicators["signal"]:
            confidence += 10
            reasons.append("Bullish MACD.")

        elif indicators["macd"] < indicators["signal"]:
            reasons.append("Bearish MACD.")

        # ==========================================
        # PRICE
        # ==========================================

        price = float(df["close"].iloc[-1])
        atr = float(indicators["atr"])

        signal = "WAIT"

        entry = round(price, 2)
        stop_loss = None
        take_profit = None

        # ==========================================
        # BUY
        # ==========================================

        if (
            indicators["trend"] == "Bullish"
            and smc["trend"] == "BULLISH"
            and confidence >= 60
        ):

            signal = "BUY"

            stop_loss = round(price - atr * 2, 2)
            take_profit = round(price + atr * 4, 2)

        # ==========================================
        # SELL
        # ==========================================

        elif (
            indicators["trend"] == "Bearish"
            and smc["trend"] == "BEARISH"
            and confidence >= 60
        ):

            signal = "SELL"

            stop_loss = round(price + atr * 2, 2)
            take_profit = round(price - atr * 4, 2)

        # ==========================================
        # RISK REWARD
        # ==========================================

        risk_reward = None

        if stop_loss is not None:

            risk = abs(entry - stop_loss)
            reward = abs(take_profit - entry)

            if risk > 0:
                risk_reward = round(reward / risk, 2)

        # ==========================================
        # RETURN
        # ==========================================

        return {

            "signal": signal,

            "confidence": confidence,

            "trend": indicators["trend"],

            "structure": smc["trend"],

            "bos_up": smc["bullish_bos"],

            "bos_down": smc["bearish_bos"],

            "choch": smc["choch"],

            "price": round(price, 2),

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit,

            "risk_reward": risk_reward,

            "ema20": round(float(indicators["ema20"]), 2),

            "ema50": round(float(indicators["ema50"]), 2),

            "ema200": round(float(indicators["ema200"]), 2),

            "rsi": round(rsi, 2),

            "macd": round(float(indicators["macd"]), 4),

            "atr": round(atr, 2),

            "reasons": reasons
        }