import MetaTrader5 as mt5
import pandas as pd

from core.indicators import Indicators


class MultiTimeframe:

    def __init__(self):

        self.indicators = Indicators()

        self.symbol = "XAUUSD"

    # =====================================================

    def get_dataframe(self, timeframe, bars=300):

        rates = mt5.copy_rates_from_pos(

            self.symbol,

            timeframe,

            0,

            bars

        )

        if rates is None:

            return None

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(

            df["time"],

            unit="s"

        )

        df.set_index(

            "time",

            inplace=True

        )

        df.rename(

            columns={

                "open": "Open",

                "high": "High",

                "low": "Low",

                "close": "Close",

                "tick_volume": "Volume"

            },

            inplace=True

        )

        return df[
            [
                "Open",
                "High",
                "Low",
                "Close",
                "Volume"
            ]
        ]

    # =====================================================

    def trend(self, timeframe):

        df = self.get_dataframe(timeframe)

        if df is None or len(df) < 220:

            return "UNKNOWN"

        ema50 = self.indicators.ema(df, 50).iloc[-1]

        ema200 = self.indicators.ema(df, 200).iloc[-1]

        price = df["Close"].iloc[-1]

        if ema50 > ema200 and price > ema50:

            return "BULLISH"

        if ema50 < ema200 and price < ema50:

            return "BEARISH"

        return "RANGING"

    # =====================================================

    def analyze(self):

        m5 = self.trend(mt5.TIMEFRAME_M5)

        m15 = self.trend(mt5.TIMEFRAME_M15)

        h1 = self.trend(mt5.TIMEFRAME_H1)

        h4 = self.trend(mt5.TIMEFRAME_H4)

        score = 0

        for tf in [m5, m15, h1, h4]:

            if tf == "BULLISH":

                score += 1

            elif tf == "BEARISH":

                score -= 1

        if score >= 3:

            overall = "BULLISH"

        elif score <= -3:

            overall = "BEARISH"

        else:

            overall = "RANGING"

        return {

            "M5": m5,

            "M15": m15,

            "H1": h1,

            "H4": h4,

            "overall": overall,

            "score": score

        }