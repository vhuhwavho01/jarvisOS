import os
from datetime import datetime


class Logger:

    def __init__(self):

        self.folder = "logs"

        os.makedirs(

            self.folder,

            exist_ok=True

        )

        self.file = os.path.join(

            self.folder,

            f"{datetime.now():%Y-%m-%d}.log"

        )

    # =====================================================

    def write(

        self,

        level,

        message

    ):

        timestamp = datetime.now().strftime(

            "%Y-%m-%d %H:%M:%S"

        )

        line = f"[{timestamp}] [{level}] {message}\n"

        with open(

            self.file,

            "a",

            encoding="utf-8"

        ) as f:

            f.write(line)

    # =====================================================

    def info(self, message):

        self.write(

            "INFO",

            message

        )

    # =====================================================

    def warning(self, message):

        self.write(

            "WARNING",

            message

        )

    # =====================================================

    def error(self, message):

        self.write(

            "ERROR",

            message

        )

    # =====================================================

    def trade(

        self,

        result

    ):

        self.write(

            "TRADE",

            f"{result['signal']} | "
            f"{result['symbol']} | "
            f"Entry={result['entry']} | "
            f"SL={result['stop_loss']} | "
            f"TP={result['take_profit']} | "
            f"Confidence={result['confidence']}%"

        )

    # =====================================================

    def exception(self, e):

        self.write(

            "EXCEPTION",

            str(e)

        )