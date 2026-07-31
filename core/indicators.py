import pandas as pd


class Indicators:

    # ==========================================
    # EMA
    # ==========================================

    def ema(self, df, period):

        return df["Close"].ewm(
            span=period,
            adjust=False
        ).mean()

    # ==========================================
    # RSI
    # ==========================================

    def rsi(self, df, period=14):

        delta = df["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(period).mean()
        avg_loss = loss.rolling(period).mean()

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))

    # ==========================================
    # MACD
    # ==========================================

    def macd(
        self,
        df,
        fast=12,
        slow=26,
        signal=9
    ):

        ema_fast = self.ema(df, fast)
        ema_slow = self.ema(df, slow)

        macd = ema_fast - ema_slow

        signal_line = macd.ewm(
            span=signal,
            adjust=False
        ).mean()

        return macd, signal_line

    # ==========================================
    # ATR
    # ==========================================

    def atr(self, df, period=14):

        high_low = df["High"] - df["Low"]

        high_close = (
            df["High"] - df["Close"].shift()
        ).abs()

        low_close = (
            df["Low"] - df["Close"].shift()
        ).abs()

        tr = pd.concat(
            [
                high_low,
                high_close,
                low_close
            ],
            axis=1
        ).max(axis=1)

        return tr.rolling(period).mean()

    # ==========================================
    # SMA
    # ==========================================

    def sma(self, df, period):

        return df["Close"].rolling(period).mean()

    # ==========================================
    # VWAP
    # ==========================================

    def vwap(self, df):

        tp = (
            df["High"] +
            df["Low"] +
            df["Close"]
        ) / 3

        return (
            tp * df["Volume"]
        ).cumsum() / df["Volume"].cumsum()

    # ==========================================
    # BOLLINGER BANDS
    # ==========================================

    def bollinger(
        self,
        df,
        period=20,
        std=2
    ):

        sma = self.sma(df, period)

        deviation = (
            df["Close"]
            .rolling(period)
            .std()
        )

        upper = sma + deviation * std
        lower = sma - deviation * std

        return upper, sma, lower

    # ==========================================
    # STOCHASTIC
    # ==========================================

    def stochastic(
        self,
        df,
        period=14
    ):

        low = df["Low"].rolling(period).min()

        high = df["High"].rolling(period).max()

        k = 100 * (
            (df["Close"] - low)
            /
            (high - low)
        )

        d = k.rolling(3).mean()

        return k, d

    # ==========================================
    # ADX
    # ==========================================

    def adx(self, df, period=14):

        plus_dm = df["High"].diff()
        minus_dm = -df["Low"].diff()

        plus_dm[plus_dm < 0] = 0
        minus_dm[minus_dm < 0] = 0

        tr = pd.concat([
            df["High"] - df["Low"],
            (df["High"] - df["Close"].shift()).abs(),
            (df["Low"] - df["Close"].shift()).abs()
        ], axis=1).max(axis=1)

        atr = tr.rolling(period).mean()

        plus_di = (
            100 *
            (plus_dm.rolling(period).mean() / atr)
        )

        minus_di = (
            100 *
            (minus_dm.rolling(period).mean() / atr)
        )

        dx = (
            (plus_di - minus_di).abs()
            /
            (plus_di + minus_di)
        ) * 100

        return dx.rolling(period).mean()