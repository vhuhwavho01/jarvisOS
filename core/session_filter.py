from datetime import datetime
import pytz


class SessionFilter:

    def __init__(self):

        self.tz = pytz.timezone("UTC")

    # ===========================================

    def current_session(self):

        now = datetime.now(self.tz)

        hour = now.hour

        if 0 <= hour < 7:
            return "ASIAN"

        elif 7 <= hour < 13:
            return "LONDON"

        elif 13 <= hour < 17:
            return "LONDON_NEWYORK"

        elif 17 <= hour < 21:
            return "NEWYORK"

        return "CLOSED"

    # ===========================================

    def trading_allowed(self):

        return self.current_session() in (

            "LONDON",

            "LONDON_NEWYORK",

            "NEWYORK"

        )

    # ===========================================

    def session_score(self):

        session = self.current_session()

        if session == "LONDON_NEWYORK":
            return 30

        if session == "LONDON":
            return 20

        if session == "NEWYORK":
            return 15

        return -20