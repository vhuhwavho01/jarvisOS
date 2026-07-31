from datetime import datetime


class TradingEngine:

    def __init__(self):

        self.symbol = "XAUUSD"

    # ==========================================
    # Get Market Data
    # ==========================================

    def get_market_data(self):

        return {

            "symbol": self.symbol,

            "price": 0.0,

            "trend": "Waiting",

            "signal": "WAIT",

            "confidence": 0,

            "risk": "Unknown",

            "support": "--",

            "resistance": "--",

            "session": self.get_session(),

            "analysis":
                "Trading Engine initialized.\n"
                "Waiting for live market data."
        }

    # ==========================================
    # Trading Session
    # ==========================================

    def get_session(self):

        hour = datetime.utcnow().hour

        if 0 <= hour < 7:
            return "Asian Session"

        elif 7 <= hour < 13:
            return "London Session"

        elif 13 <= hour < 22:
            return "New York Session"

        return "Market Closed"