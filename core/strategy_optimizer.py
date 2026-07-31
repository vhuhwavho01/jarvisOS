import itertools


class StrategyOptimizer:

    def __init__(self):

        self.best = None

        self.best_profit = float("-inf")

    # =====================================================

    def optimize(

        self,

        backtester,

        dataframe

    ):

        ema_fast = [20, 30, 50]

        ema_slow = [100, 150, 200]

        rr_values = [1.5, 2.0, 2.5, 3.0]

        risk_values = [0.5, 1.0, 2.0]

        for fast, slow, rr, risk in itertools.product(

            ema_fast,

            ema_slow,

            rr_values,

            risk_values

        ):

            if fast >= slow:

                continue

            backtester.engine.indicators.ema_fast = fast

            backtester.engine.indicators.ema_slow = slow

            backtester.engine.risk.default_rr = rr

            backtester.engine.risk.risk_percent = risk

            result = backtester.run(dataframe)

            profit = result["Profit"]

            if profit > self.best_profit:

                self.best_profit = profit

                self.best = {

                    "ema_fast": fast,

                    "ema_slow": slow,

                    "risk_reward": rr,

                    "risk_percent": risk,

                    "profit": profit,

                    "win_rate": result["Win Rate"],

                    "trades": result["Trades"]

                }

        return self.best

    # =====================================================

    def summary(self):

        return self.best