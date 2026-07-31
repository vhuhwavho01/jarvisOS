import threading
import time

from core.trade_manager import TradeManager
from core.jarvis_engine import JarvisEngine


class AutoTrader:

    def __init__(self):

        self.engine = JarvisEngine()

        self.trade_manager = TradeManager()

        self.enabled = False

        self.symbol = "XAUUSD"

        self.lot = 0.01

        self.interval = 5

        self.thread = None

    # ======================================================

    def start(self):

        if self.enabled:
            return

        self.enabled = True

        self.thread = threading.Thread(

            target=self.run,

            daemon=True

        )

        self.thread.start()

    # ======================================================

    def stop(self):

        self.enabled = False

    # ======================================================

    def run(self):

        while self.enabled:

            try:

                positions = self.trade_manager.open_positions()

                if len(positions) == 0:

                    signal = self.engine.analyze()

                    if signal and signal["status"]:

                        self.execute(signal)

            except Exception as e:

                print("Auto Trader:", e)

            time.sleep(self.interval)

    # ======================================================

    def execute(self, signal):

        direction = signal["signal"]

        entry = signal["entry"]

        sl = signal["stop_loss"]

        tp = signal["take_profit"]

        if direction in (

            "BUY",

            "STRONG_BUY"

        ):

            self.trade_manager.buy(

                self.symbol,

                self.lot,

                sl,

                tp

            )

        elif direction in (

            "SELL",

            "STRONG_SELL"

        ):

            self.trade_manager.sell(

                self.symbol,

                self.lot,

                sl,

                tp

            )

    # ======================================================

    def set_symbol(

        self,

        symbol

    ):

        self.symbol = symbol

    # ======================================================

    def set_lot(

        self,

        lot

    ):

        self.lot = lot

    # ======================================================

    def running(self):

        return self.enabled