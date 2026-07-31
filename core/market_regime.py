class MarketRegime:

    def __init__(self):

        self.atr_period = 14

        self.adx_threshold = 25

    # =====================================================

    def detect(self, df):

        result = {

            "regime": "RANGE",

            "strength": 0,

            "volatility": 0,

            "trend": "RANGE"

        }

        try:

            if df is None or len(df) < 50:

                return result

            high = df["High"]
            low = df["Low"]
            close = df["Close"]

            # -------------------------------
            # ATR
            # -------------------------------

            tr1 = high - low
            tr2 = (high - close.shift()).abs()
            tr3 = (low - close.shift()).abs()

            tr = tr1.combine(tr2, max).combine(tr3, max)

            atr = tr.rolling(self.atr_period).mean()

            atr_value = float(atr.iloc[-1])

            result["volatility"] = round(atr_value, 2)

            # -------------------------------
            # EMA Trend
            # -------------------------------

            ema50 = close.ewm(span=50).mean().iloc[-1]
            ema200 = close.ewm(span=200).mean().iloc[-1]

            if ema50 > ema200:

                trend = "BULLISH"

            elif ema50 < ema200:

                trend = "BEARISH"

            else:

                trend = "RANGE"

            result["trend"] = trend

            # -------------------------------
            # Trend Strength
            # -------------------------------

            price_change = abs(close.iloc[-1] - close.iloc[-20])

            strength = 0

            if atr_value > 0:

                strength = (price_change / atr_value)

            result["strength"] = round(strength, 2)

            # -------------------------------
            # Market Regime
            # -------------------------------

            if strength >= 5:

                result["regime"] = "TREND"

            else:

                result["regime"] = "RANGE"

            return result

        except Exception as e:

            result["error"] = str(e)

            return result