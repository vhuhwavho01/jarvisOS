import MetaTrader5 as mt5


class BreakEven:

    def __init__(self):

        # Move SL to entry after this many points profit
        self.trigger_points = 200

        # Lock a few points profit
        self.offset_points = 10

    # =====================================================

    def update(self):

        positions = mt5.positions_get()

        if positions is None:
            return

        for position in positions:

            symbol = position.symbol

            info = mt5.symbol_info(symbol)

            tick = mt5.symbol_info_tick(symbol)

            if info is None or tick is None:
                continue

            point = info.point

            # ---------------- BUY ----------------

            if position.type == mt5.POSITION_TYPE_BUY:

                profit_points = (tick.bid - position.price_open) / point

                if profit_points >= self.trigger_points:

                    new_sl = position.price_open + (
                        self.offset_points * point
                    )

                    if position.sl < new_sl:

                        self.modify(position, new_sl)

            # ---------------- SELL ----------------

            else:

                profit_points = (position.price_open - tick.ask) / point

                if profit_points >= self.trigger_points:

                    new_sl = position.price_open - (
                        self.offset_points * point
                    )

                    if position.sl == 0 or position.sl > new_sl:

                        self.modify(position, new_sl)

    # =====================================================

    def modify(self, position, stop_loss):

        request = {

            "action": mt5.TRADE_ACTION_SLTP,

            "position": position.ticket,

            "symbol": position.symbol,

            "sl": round(stop_loss, 2),

            "tp": position.tp

        }

        result = mt5.order_send(request)

        if result is not None:

            print(
                f"Break-even updated for ticket {position.ticket}"
            )