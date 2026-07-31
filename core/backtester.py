import pandas as pd

from core.jarvis_engine import JarvisEngine
from core.risk_manager import RiskManager


class BackTester:

    def __init__(self):

        self.engine = JarvisEngine()
        self.risk = RiskManager()

        self.balance = 10000.0
        self.start_balance = 10000.0

        self.total_trades = 0
        self.wins = 0
        self.losses = 0

        self.history = []

    # =====================================================

    def run(self, df):

        self.balance = self.start_balance

        self.total_trades = 0
        self.wins = 0
        self.losses = 0
        self.history = []

        for i in range(250, len(df) - 1):

            data = df.iloc[: i + 1]

            result = self.engine.analyze_gold_from_dataframe(data)

            if not result["status"]:
                continue

            signal = result["signal"]

            if signal == "WAIT":
                continue

            entry = result["entry"]
            sl = result["stop_loss"]
            tp = result["take_profit"]

            next_bar = df.iloc[i + 1]

            if signal == "BUY":

                if next_bar.Low <= sl:

                    profit = -100

                elif next_bar.High >= tp:

                    profit = 200

                else:

                    continue

            else:

                if next_bar.High >= sl:

                    profit = -100

                elif next_bar.Low <= tp:

                    profit = 200

                else:

                    continue

            self.balance += profit

            self.total_trades += 1

            if profit > 0:

                self.wins += 1

            else:

                self.losses += 1

            self.history.append({

                "Signal": signal,

                "Entry": entry,

                "SL": sl,

                "TP": tp,

                "Profit": profit,

                "Balance": self.balance

            })

        return self.summary()

    # =====================================================

    def summary(self):

        win_rate = 0

        if self.total_trades > 0:

            win_rate = round(

                (self.wins / self.total_trades) * 100,

                2

            )

        return {

            "Starting Balance": self.start_balance,

            "Ending Balance": round(self.balance, 2),

            "Profit": round(

                self.balance - self.start_balance,

                2

            ),

            "Trades": self.total_trades,

            "Wins": self.wins,

            "Losses": self.losses,

            "Win Rate": win_rate,

            "History": self.history

        }