import math


class RiskManager:

    def __init__(self):

        self.default_rr = 2.0

    # =====================================================

    def calculate(

        self,

        signal,

        entry,

        atr,

        rr=None

    ):

        if rr is None:

            rr = self.default_rr

        atr = max(float(atr), 0.10)

        if signal in ("BUY", "STRONG_BUY"):

            stop_loss = entry - (atr * 2)

            take_profit = entry + ((entry - stop_loss) * rr)

        elif signal in ("SELL", "STRONG_SELL"):

            stop_loss = entry + (atr * 2)

            take_profit = entry - ((stop_loss - entry) * rr)

        else:

            stop_loss = entry

            take_profit = entry

        return {

            "entry": round(entry, 2),

            "stop_loss": round(stop_loss, 2),

            "take_profit": round(take_profit, 2),

            "risk_reward": rr

        }

    # =====================================================

    def calculate_lot(

        self,

        balance,

        risk_percent,

        stop_loss_points,

        pip_value=10

    ):

        if stop_loss_points <= 0:

            return 0.01

        risk_amount = balance * (risk_percent / 100)

        lot = risk_amount / (stop_loss_points * pip_value)

        lot = max(0.01, lot)

        return round(lot, 2)