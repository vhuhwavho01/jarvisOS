from datetime import datetime, timedelta
import requests


class NewsService:

    def __init__(self):

        self.events = []

        self.url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"

    # =====================================================

    def update(self):

        self.events.clear()

        try:

            response = requests.get(

                self.url,

                timeout=10

            )

            data = response.json()

        except Exception:

            return False

        for item in data:

            try:

                if item.get("impact", "").lower() != "high":
                    continue

                dt = datetime.strptime(

                    f"{item['date']} {item['time']}",

                    "%Y-%m-%d %H:%M"

                )

                self.events.append({

                    "currency": item.get("country", ""),

                    "title": item.get("title", ""),

                    "impact": item.get("impact", ""),

                    "time": dt

                })

            except Exception:

                continue

        self.events.sort(

            key=lambda x: x["time"]

        )

        return True

    # =====================================================

    def high_impact_active(self):

        now = datetime.utcnow()

        for event in self.events:

            start = event["time"] - timedelta(minutes=30)

            end = event["time"] + timedelta(minutes=30)

            if start <= now <= end:

                return True

        return False

    # =====================================================

    def next_event(self):

        now = datetime.utcnow()

        future = [

            e for e in self.events

            if e["time"] > now

        ]

        if not future:

            return None

        return future[0]

    # =====================================================

    def summary(self):

        return {

            "blocked": self.high_impact_active(),

            "next": self.next_event(),

            "events": self.events

        }