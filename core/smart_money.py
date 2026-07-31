import numpy as np


class SmartMoney:

    def __init__(self):

        self.swing = 3

    # =====================================================

    def analyze(self, df):

        return {

            "bos": self.detect_bos(df),

            "choch": self.detect_choch(df),

            "order_block": self.detect_order_block(df),

            "fvg": self.detect_fvg(df),

            "equal_highs": self.equal_highs(df),

            "equal_lows": self.equal_lows(df),

            "liquidity_sweep": self.detect_liquidity(df),

            "premium_discount": self.premium_discount(df)

        }

    # =====================================================

    def swing_highs(self, df):

        highs = []

        h = df["High"].values

        s = self.swing

        for i in range(s, len(df)-s):

            if h[i] == max(h[i-s:i+s+1]):

                highs.append((i, h[i]))

        return highs

    # =====================================================

    def swing_lows(self, df):

        lows = []

        l = df["Low"].values

        s = self.swing

        for i in range(s, len(df)-s):

            if l[i] == min(l[i-s:i+s+1]):

                lows.append((i, l[i]))

        return lows

    # =====================================================

    def detect_bos(self, df):

        highs = self.swing_highs(df)

        lows = self.swing_lows(df)

        close = df["Close"].iloc[-1]

        if highs:

            last_high = highs[-1][1]

            if close > last_high:

                return "Bullish"

        if lows:

            last_low = lows[-1][1]

            if close < last_low:

                return "Bearish"

        return None

    # =====================================================

    def detect_choch(self, df):

        highs = self.swing_highs(df)

        lows = self.swing_lows(df)

        if len(highs) < 2 or len(lows) < 2:

            return None

        if highs[-1][1] < highs[-2][1]:

            return "Bearish"

        if lows[-1][1] > lows[-2][1]:

            return "Bullish"

        return None

    # =====================================================

    def detect_order_block(self, df):

        candles = df.tail(30)

        biggest = None

        body = 0

        for _, row in candles.iterrows():

            size = abs(row["Close"] - row["Open"])

            if size > body:

                body = size

                biggest = row

        if biggest is None:

            return None

        block_type = (

            "Bullish"

            if biggest["Close"] < biggest["Open"]

            else "Bearish"

        )

        return {

            "type": block_type,

            "high": round(biggest["High"], 2),

            "low": round(biggest["Low"], 2)

        }

    # =====================================================

    def detect_fvg(self, df):

        for i in range(len(df)-3, 1, -1):

            c1 = df.iloc[i-2]

            c2 = df.iloc[i-1]

            c3 = df.iloc[i]

            if c3["Low"] > c1["High"]:

                return {

                    "type": "Bullish",

                    "high": round(c3["Low"], 2),

                    "low": round(c1["High"], 2)

                }

            if c3["High"] < c1["Low"]:

                return {

                    "type": "Bearish",

                    "high": round(c1["Low"], 2),

                    "low": round(c3["High"], 2)

                }

        return None

    # =====================================================

    def equal_highs(self, df):

        highs = self.swing_highs(df)

        if len(highs) < 2:

            return False

        return abs(highs[-1][1] - highs[-2][1]) < 0.50

    # =====================================================

    def equal_lows(self, df):

        lows = self.swing_lows(df)

        if len(lows) < 2:

            return False

        return abs(lows[-1][1] - lows[-2][1]) < 0.50

    # =====================================================

    def detect_liquidity(self, df):

        last = df.iloc[-1]

        prev_high = df["High"].tail(20).max()

        prev_low = df["Low"].tail(20).min()

        if last["High"] > prev_high and last["Close"] < prev_high:

            return "Bearish Sweep"

        if last["Low"] < prev_low and last["Close"] > prev_low:

            return "Bullish Sweep"

        return None

    # =====================================================

    def premium_discount(self, df):

        high = df["High"].tail(100).max()

        low = df["Low"].tail(100).min()

        equilibrium = (high + low) / 2

        price = df["Close"].iloc[-1]

        return "Premium" if price > equilibrium else "Discount"