import MetaTrader5 as mt5


class OrderManager:

    def __init__(self):

        pass

    # =====================================================

    def positions(self, symbol=None):

        if symbol:

            return mt5.positions_get(symbol=symbol)

        return mt5.positions_get()

    # =====================================================

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

            "deviation": 20,

            "magic": 2026001,

            "comment": "JARVIS Close"

        }

        return mt5.order_send(request)

    # =====================================================

    def partial_close(self, position, volume):

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

            "volume": volume,

            "type": order_type,

            "price": price,

            "deviation": 20,

            "magic": 2026001,

            "comment": "JARVIS Partial Close"

        }

        return mt5.order_send(request)

    # =====================================================

    def modify(self, ticket, symbol, stop_loss, take_profit):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": ticket,

            "symbol": symbol,

            "sl": stop_loss,

            "tp": take_profit

        }

        return mt5.order_send(request)

    # =====================================================

    def close_all(self):

        positions = mt5.positions_get()

        if positions is None:

            return

        for position in positions:

            self.close_position(position)