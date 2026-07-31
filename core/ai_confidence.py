class AIConfidence:

    def __init__(self):
        pass

    # =====================================================
    # SCORE SIGNAL
    # =====================================================

    def calculate(self, analysis):

        score = 0
        reasons = []

        # ------------------------------------------
        # EMA
        # ------------------------------------------

        if analysis.get("ema_bullish"):

            score += 15
            reasons.append("Bullish EMA Alignment")

        elif analysis.get("ema_bearish"):

            score += 15
            reasons.append("Bearish EMA Alignment")

        # ------------------------------------------
        # MARKET STRUCTURE
        # ------------------------------------------

        structure = analysis.get("structure")

        if structure == "BULLISH":

            score += 20
            reasons.append("Bullish Structure")

        elif structure == "BEARISH":

            score += 20
            reasons.append("Bearish Structure")

        # ------------------------------------------
        # BOS
        # ------------------------------------------

        if analysis.get("bos"):

            score += 15
            reasons.append("Break Of Structure")

        # ------------------------------------------
        # CHOCH
        # ------------------------------------------

        if analysis.get("choch"):

            score += 15
            reasons.append("CHoCH Confirmation")

        # ------------------------------------------
        # RSI
        # ------------------------------------------

        rsi = analysis.get("rsi", 50)

        signal = analysis.get("signal")

        if signal == "BUY":

            if rsi < 35:

                score += 10
                reasons.append("RSI Oversold")

        if signal == "SELL":

            if rsi > 65:

                score += 10
                reasons.append("RSI Overbought")

        # ------------------------------------------
        # MACD
        # ------------------------------------------

        if analysis.get("macd_bullish"):

            score += 10
            reasons.append("Bullish MACD")

        if analysis.get("macd_bearish"):

            score += 10
            reasons.append("Bearish MACD")

        # ------------------------------------------
        # ORDER BLOCK
        # ------------------------------------------

        if analysis.get("order_block"):

            score += 10
            reasons.append("Order Block")

        # ------------------------------------------
        # FAIR VALUE GAP
        # ------------------------------------------

        if analysis.get("fvg"):

            score += 10
            reasons.append("Fair Value Gap")

        # ------------------------------------------
        # LIQUIDITY
        # ------------------------------------------

        if analysis.get("liquidity_sweep"):

            score += 10
            reasons.append("Liquidity Sweep")

        # ------------------------------------------
        # ATR
        # ------------------------------------------

        if analysis.get("atr_ok"):

            score += 5
            reasons.append("Healthy Volatility")

        # ------------------------------------------

        if score > 100:
            score = 100

        return {
            "confidence": score,
            "reasons": reasons
        }