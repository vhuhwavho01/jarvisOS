import MetaTrader5 as mt5

import pandas as pd

from core.jarvis_engine import JarvisEngine


class ChartController:

    def __init__(self):

        self.symbol = "XAUUSD"

        self.timeframe = mt5.TIMEFRAME_M5

        self.candles = 300

        self.engine = JarvisEngine()

    # =====================================================

    def get_dataframe(self):

        rates = mt5.copy_rates_from_pos(

            self.symbol,

            self.timeframe,

            0,

            self.candles

        )

        if rates is None:

            return None

        df = pd.DataFrame(rates)

        df["Time"] = pd.to_datetime(

            df["time"],

            unit="s"

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

        return df

    # =====================================================

    def refresh(self, chart):

        df = self.get_dataframe()

        if df is None:

            return

        chart.draw_chart(df)

        result = self.engine.analyze_dataframe(df)

        if not result["status"]:

            chart.refresh()

            return

        institutional = result["institutional"]

        price = df.Close.iloc[-1]

        # ==========================================
        # BUY / SELL SIGNAL
        # ==========================================

        if result["signal"] in (

            "BUY",

            "STRONG_BUY"

        ):

            chart.draw_buy(price)

        elif result["signal"] in (

            "SELL",

            "STRONG_SELL"

        ):

            chart.draw_sell(price)

        # ==========================================
        # ORDER BLOCK
        # ==========================================

        ob = institutional["order_blocks"]["nearest"]

        if ob:

            chart.draw_order_block(

                ob["high"],

                ob["low"]

            )

        # ==========================================
        # FAIR VALUE GAP
        # ==========================================

        fvg = institutional["fair_value_gap"]["nearest"]

        if fvg:

            chart.draw_fvg(

                fvg["high"],

                fvg["low"]

            )

        # ==========================================
        # LIQUIDITY
        # ==========================================

        buy_side = institutional["liquidity"]["buy_side"]

        sell_side = institutional["liquidity"]["sell_side"]

        if buy_side:

            chart.draw_liquidity(

                buy_side["price"]

            )

        if sell_side:

            chart.draw_liquidity(

                sell_side["price"]

            )

        # ==========================================
        # ENTRY / SL / TP
        # ==========================================

        chart.draw_horizontal(

            result["entry"],

            "white",

            "ENTRY"

        )

        chart.draw_horizontal(

            result["stop_loss"],

            "red",

            "SL"

        )

        chart.draw_horizontal(

            result["take_profit"],

            "lime",

            "TP"

        )

        chart.refresh()