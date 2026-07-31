import MetaTrader5 as mt5


class PositionManager:

    def __init__(self):
        if not mt5.initialize():
            raise Exception("Failed to connect to MT5")

    def get_positions(self, symbol=None):

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            return []

        data = []

        for pos in positions:

            trade_type = "BUY" if pos.type == mt5.POSITION_TYPE_BUY else "SELL"

            data.append({
                "ticket": pos.ticket,
                "symbol": pos.symbol,
                "type": trade_type,
                "volume": pos.volume,
                "price": round(pos.price_open, 2),
                "sl": round(pos.sl, 2) if pos.sl else 0,
                "tp": round(pos.tp, 2) if pos.tp else 0,
                "profit": round(pos.profit, 2)
            })

        return data