from datetime import datetime, timedelta


class NewsFilter:

    def __init__(self):

        self.enabled = True

        self.high_impact_minutes = 30

        self.events = []

    # =====================================================

    def add_event(

        self,

        event_name,

        event_time,

        impact="HIGH"

    ):

        self.events.append(

            {

                "name": event_name,

                "time": event_time,

                "impact": impact.upper()

            }

        )

    # =====================================================

    def clear_events(self):

        self.events.clear()

    # =====================================================

    def trading_allowed(self):

        if not self.enabled:

            return True

        now = datetime.utcnow()

        for event in self.events:

            if event["impact"] != "HIGH":

                continue

            start = event["time"] - timedelta(

                minutes=self.high_impact_minutes

            )

            end = event["time"] + timedelta(

                minutes=self.high_impact_minutes

            )

            if start <= now <= end:

                return False

        return True

    # =====================================================

    def next_event(self):

        now = datetime.utcnow()

        future = [

            e for e in self.events

            if e["time"] > now

        ]

        if not future:

            return None

        future.sort(

            key=lambda x: x["time"]

        )

        return future[0]

    # =====================================================

    def status(self):

        event = self.next_event()

        if event is None:

            return {

                "allowed": self.trading_allowed(),

                "message": "No scheduled high-impact news."

            }

        return {

            "allowed": self.trading_allowed(),

            "event": event["name"],

            "time": event["time"],

            "impact": event["impact"]

        }

    # =====================================================

    def enable(self):

        self.enabled = True

    def disable(self):

        self.enabled = False