import customtkinter as ctk
import MetaTrader5 as mt5
import threading
import time
import traceback

from ui.main_window import MainWindow
from core.jarvis_engine import JarvisEngine


class JarvisApp:

    def __init__(self):

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        if not mt5.initialize():
            raise Exception("Failed to initialize MetaTrader 5.")

        self.engine = JarvisEngine()

        self.window = MainWindow()

        self.running = True

        self.thread = threading.Thread(
            target=self.live_update_loop,
            daemon=True
        )

        self.thread.start()

    # ======================================================

    def live_update_loop(self):

        while self.running:

            try:

                result = self.engine.analyze()

                if result is None:
                    time.sleep(2)
                    continue

                if hasattr(self.window, "dashboard"):

                    self.window.dashboard.update_dashboard(result)

                if hasattr(self.window, "trading"):

                    self.window.trading.update_signal(result)

                positions = mt5.positions_get()

                if positions is None:
                    positions = []

                if hasattr(self.window, "trading"):

                    self.window.trading.load_positions(positions)

            except Exception:

                print("\n" + "=" * 70)
                print("LIVE UPDATE ERROR")
                print("=" * 70)

                traceback.print_exc()

                print("=" * 70 + "\n")

            time.sleep(2)

    # ======================================================

    def run(self):

        try:

            self.window.mainloop()

        finally:

            self.running = False

            mt5.shutdown()


if __name__ == "__main__":

    app = JarvisApp()

    app.run()