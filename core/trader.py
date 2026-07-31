import MetaTrader5 as mt5


class Trader:

    def __init__(self):

        if not mt5.initialize():
            raise Exception("Failed to initialize MT5")

        self.deviation = 20
        self.magic = 987654

    # =====================================================
    # BUY
    # =====================================================

    def buy(self, symbol, volume, sl=None, tp=None):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return None

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": float(volume),

            "type": mt5.ORDER_TYPE_BUY,

            "price": tick.ask,

            "sl": sl if sl else 0,

            "tp": tp if tp else 0,

            "deviation": self.deviation,

            "magic": self.magic,

            "comment": "JARVIS BUY",

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        return mt5.order_send(request)

    # =====================================================
    # SELL
    # =====================================================

    def sell(self, symbol, volume, sl=None, tp=None):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return None

        request = {

            "action": mt5.TRADE_ACTION_DEAL,

            "symbol": symbol,

            "volume": float(volume),

            "type": mt5.ORDER_TYPE_SELL,

            "price": tick.bid,

            "sl": sl if sl else 0,

            "tp": tp if tp else 0,

            "deviation": self.deviation,

            "magic": self.magic,

            "comment": "JARVIS SELL",

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        return mt5.order_send(request)

    # =====================================================
    # CLOSE POSITION
    # =====================================================

    def close(self, ticket):

        positions = mt5.positions_get(ticket=ticket)

        if not positions:
            return None

        position = positions[0]

        tick = mt5.symbol_info_tick(position.symbol)

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

            "comment": "JARVIS CLOSE",

            "type_time": mt5.ORDER_TIME_GTC,

            "type_filling": mt5.ORDER_FILLING_IOC

        }

        return mt5.order_send(request)

    # =====================================================
    # MODIFY SL / TP
    # =====================================================

    def modify(self, ticket, sl=None, tp=None):

        positions = mt5.positions_get(ticket=ticket)

        if not positions:
            return None

        position = positions[0]

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": ticket,

            "symbol": position.symbol,

            "sl": sl if sl is not None else position.sl,

            "tp": tp if tp is not None else position.tp

        }

        return mt5.order_send(request)

    # =====================================================
    # OPEN POSITIONS
    # =====================================================

    def positions(self, symbol=None):

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        return [] if positions is None else list(positions)

    # =====================================================
    # CLOSE ALL
    # =====================================================

    def close_all(self):

        results = []

        for position in self.positions():

            results.append(
                self.close(position.ticket)
            )

        return results