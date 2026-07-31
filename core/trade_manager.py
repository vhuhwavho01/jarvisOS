import MetaTrader5 as mt5
import math


class TradeManager:

    def __init__(self):

        self.magic = 2026001

        self.deviation = 20

    # ======================================================

    def buy(

        self,

        symbol,

        volume,

        sl,

        tp,

        comment="JARVIS BUY"

    ):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            return None

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": volume,

            "type": mt5.ORDER_TYPE_BUY,

            "price": tick.ask,

            "sl": sl,

            "tp": tp,

            "deviation": self.deviation,

            "magic": self.magic,

            "comment": comment,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        return mt5.order_send(request)

    # ======================================================

    def sell(

        self,

        symbol,

        volume,

        sl,

        tp,

        comment="JARVIS SELL"

    ):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            return None

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": volume,

            "type": mt5.ORDER_TYPE_SELL,

            "price": tick.bid,

            "sl": sl,

            "tp": tp,

            "deviation": self.deviation,

            "magic": self.magic,

            "comment": comment,

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        return mt5.order_send(request)

    # ======================================================

    def close_position(self, position):

        tick = mt5.symbol_info_tick(position.symbol)

        if tick is None:

            return None

        if position.type == mt5.POSITION_TYPE_BUY:

            order_type = mt5.ORDER_TYPE_SELL
            price = tick.bid

        else:

            order_type = mt5.ORDER_TYPE_BUY
            price = tick.ask

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "position": position.ticket,

            "symbol": position.symbol,

            "volume": position.volume,

            "type": order_type,

            "price": price,

            "deviation": self.deviation,

            "magic": self.magic,

            "comment": "JARVIS CLOSE"

        }

        return mt5.order_send(request)

    # ======================================================

    def close_all(self):

        positions = mt5.positions_get()

        if positions is None:

            return

        for position in positions:

            self.close_position(position)

    # ======================================================

    def modify(

        self,

        ticket,

        symbol,

        sl,

        tp

    ):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": ticket,

            "symbol": symbol,

            "sl": sl,

            "tp": tp

        }

        return mt5.order_send(request)

    # ======================================================

    def calculate_lot_size(

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

    # ======================================================

    def open_positions(self):

        positions = mt5.positions_get()

        if positions is None:

            return []

        return list(positions)

    # ======================================================

    def account_info(self):

        return mt5.account_info()