import pandas as pd
import numpy as np


class MarketStructure:

    def __init__(self):

        self.swing = 5

    # =====================================================

    def analyze(self, df):

        result = {

            "trend": "RANGE",

            "bos": False,

            "choch": False,

            "last_high": None,

            "last_low": None

        }

        try:

            highs = df["High"]
            lows = df["Low"]

            swing_highs = []
            swing_lows = []

            for i in range(self.swing, len(df) - self.swing):

                if highs.iloc[i] == max(highs.iloc[i-self.swing:i+self.swing+1]):

                    swing_highs.append((i, highs.iloc[i]))

                if lows.iloc[i] == min(lows.iloc[i-self.swing:i+self.swing+1]):

                    swing_lows.append((i, lows.iloc[i]))

            if len(swing_highs) >= 2:

                result["last_high"] = swing_highs[-1][1]

            if len(swing_lows) >= 2:

                result["last_low"] = swing_lows[-1][1]

            close = df["Close"].iloc[-1]

            if result["last_high"] and close > result["last_high"]:

                result["bos"] = True
                result["trend"] = "BULLISH"

            elif result["last_low"] and close < result["last_low"]:

                result["bos"] = True
                result["trend"] = "BEARISH"

            elif len(swing_highs) >= 2 and len(swing_lows) >= 2:

                if swing_highs[-1][1] > swing_highs[-2][1] and \
                   swing_lows[-1][1] > swing_lows[-2][1]:

                    result["trend"] = "BULLISH"

                elif swing_highs[-1][1] < swing_highs[-2][1] and \
                     swing_lows[-1][1] < swing_lows[-2][1]:

                    result["trend"] = "BEARISH"

                else:

                    result["trend"] = "RANGE"

            return result

        except Exception as e:

            result["error"] = str(e)

            return result