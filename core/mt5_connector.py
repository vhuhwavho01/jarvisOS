import MetaTrader5 as mt5


class MT5Connector:

    def __init__(self):

        if not mt5.initialize():
            raise Exception("MT5 initialization failed")

    def account(self):

        return mt5.account_info()

    def symbol_info(self, symbol):

        return mt5.symbol_info(symbol)

    def tick(self, symbol):

        return mt5.symbol_info_tick(symbol)

    def rates(self, symbol, timeframe, bars):

        return mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )

    def positions(self, symbol=None):

        if symbol:
            return mt5.positions_get(symbol=symbol)

        return mt5.positions_get()

    def orders(self):

        return mt5.orders_get()

    def history(self):

        return mt5.history_deals_get()

    def shutdown(self):

        mt5.shutdown()