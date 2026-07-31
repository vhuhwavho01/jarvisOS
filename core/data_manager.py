import MetaTrader5 as mt5
import pandas as pd


class DataManager:

    def __init__(self):

        self.symbol = "XAUUSD"

        self.timeframe = mt5.TIMEFRAME_M5

        self.candles = 500

    # =====================================================

    def set_symbol(self, symbol):

        self.symbol = symbol

    # =====================================================

    def set_timeframe(self, timeframe):

        self.timeframe = timeframe

    # =====================================================

    def get_rates(self):

        try:

            rates = mt5.copy_rates_from_pos(

                self.symbol,

                self.timeframe,

                0,

                self.candles

            )

            if rates is None:

                return None

            return rates

        except Exception:

            return None

    # =====================================================

    def get_dataframe(self):

        rates = self.get_rates()

        if rates is None:

            return None

        df = pd.DataFrame(rates)

        if df.empty:

            return None

        df.rename(

            columns={

                "time": "Time",

                "open": "Open",

                "high": "High",

                "low": "Low",

                "close": "Close",

                "tick_volume": "Volume"

            },

            inplace=True

        )

        df["Time"] = pd.to_datetime(

            df["Time"],

            unit="s"

        )

        df.sort_values(

            "Time",

            inplace=True

        )

        df.reset_index(

            drop=True,

            inplace=True

        )

        return df

    # =====================================================

    def last_price(self):

        tick = mt5.symbol_info_tick(

            self.symbol

        )

        if tick is None:

            return None

        return {

            "bid": tick.bid,

            "ask": tick.ask,

            "spread": tick.ask - tick.bid

        }

    # =====================================================

    def symbol_info(self):

        return mt5.symbol_info(

            self.symbol

        )