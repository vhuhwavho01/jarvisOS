import MetaTrader5 as mt5


class TrailingStop:

    def __init__(self):

        self.distance = 300      # points

    # =====================================================

    def update(self):

        positions = mt5.positions_get()

        if positions is None:

            return

        for position in positions:

            symbol = position.symbol

            tick = mt5.symbol_info_tick(symbol)

            if tick is None:

                continue

            if position.type == mt5.POSITION_TYPE_BUY:

                new_sl = tick.bid - self.distance * mt5.symbol_info(symbol).point

                if position.sl == 0 or new_sl > position.sl:

                    self.modify(position, new_sl)

            else:

                new_sl = tick.ask + self.distance * mt5.symbol_info(symbol).point

                if position.sl == 0 or new_sl < position.sl:

                    self.modify(position, new_sl)

    # =====================================================

    def modify(self, position, stop_loss):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": position.ticket,

            "symbol": position.symbol,

            "sl": stop_loss,

            "tp": position.tp

        }

        mt5.order_send(request)