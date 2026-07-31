import json
import os


class Config:

    FILE = "config.json"

    DEFAULT = {

        "symbol": "XAUUSD",

        "timeframe": "M5",

        "risk_percent": 1.0,

        "risk_reward": 2.0,

        "minimum_confidence": 80,

        "trade_interval": 60,

        "auto_trade": False,

        "break_even": True,

        "trailing_stop": True,

        "telegram_enabled": False,

        "telegram_token": "",

        "telegram_chat_id": "",

        "discord_enabled": False,

        "discord_webhook": "",

        "mt5_login": 0,

        "mt5_password": "",

        "mt5_server": ""

    }

    # =====================================================

    def __init__(self):

        if not os.path.exists(self.FILE):

            self.save(self.DEFAULT)

        self.data = self.load()

    # =====================================================

    def load(self):

        try:

            with open(

                self.FILE,

                "r",

                encoding="utf-8"

            ) as f:

                return json.load(f)

        except Exception:

            return self.DEFAULT.copy()

    # =====================================================

    def save(self, data=None):

        if data is None:

            data = self.data

        with open(

            self.FILE,

            "w",

            encoding="utf-8"

        ) as f:

            json.dump(

                data,

                f,

                indent=4

            )

    # =====================================================

    def get(

        self,

        key,

        default=None

    ):

        return self.data.get(

            key,

            default

        )

    # =====================================================

    def set(

        self,

        key,

        value

    ):

        self.data[key] = value

        self.save()

    # =====================================================

    def reset(self):

        self.data = self.DEFAULT.copy()

        self.save()

    # =====================================================

    def all(self):

        return self.data