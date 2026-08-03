import customtkinter as ctk
import MetaTrader5 as mt5
import threading
import time
import traceback
import logging

from ui.main_window import MainWindow
from core.jarvis_engine import JarvisEngine

LOG = logging.getLogger("jarvis.app")


class JarvisApp:

    def __init__(self):

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Try to initialize MT5 but do not abort startup if it fails
        self.mt5_initialized = False
        try:
            ok = mt5.initialize()
        except Exception as e:
            ok = False
            LOG.warning("mt5.initialize() raised: %s", e, exc_info=True)

        if not ok:
            LOG.warning("Failed to initialize MetaTrader 5. Running in offline/degraded mode.")
        else:
            self.mt5_initialized = True
            LOG.info("MetaTrader5 initialized successfully")

        self.engine = JarvisEngine()

        self.window = MainWindow()

        self.running = True

        self.thread = threading.Thread(
            target=self.live_update_loop,
            daemon=True,
            name="LiveUpdate",
        )

        self.thread.start()

    # ======================================================

    def live_update_loop(self):

        while self.running:

            try:

                result = self.engine.analyze()

                LOG.debug("Analysis completed: %s", repr(result))

                if result is None:
                    time.sleep(2)
                    continue

                # Schedule dashboard update on the UI thread
                try:
                    if hasattr(self.window, "dashboard"):
                        # update_dashboard will schedule an after() callback internally
                        self.window.dashboard.update_dashboard(result)
                        LOG.info("Dashboard updated: signal=%s confidence=%s", result.get("signal"), result.get("confidence"))
                except Exception:
                    LOG.exception("Failed to update dashboard")

                # Trading page update
                try:
                    if hasattr(self.window, "trading"):
                        self.window.trading.update_signal(result)
                except Exception:
                    LOG.exception("Failed to update trading page")

                # Positions (only when mt5 initialized)
                positions = []
                if self.mt5_initialized:
                    try:
                        positions = mt5.positions_get()
                        if positions is None:
                            positions = []
                    except Exception:
                        LOG.exception("mt5.positions_get() failed")
                        positions = []

                try:
                    if hasattr(self.window, "trading"):
                        self.window.trading.load_positions(positions)
                except Exception:
                    LOG.exception("Failed to load positions into trading page")

            except Exception:

                LOG.exception("LIVE UPDATE ERROR")

            time.sleep(2)

    # ======================================================

    def run(self):

        try:

            self.window.mainloop()

        finally:

            self.running = False

            if self.mt5_initialized:
                try:
                    mt5.shutdown()
                except Exception:
                    LOG.exception("mt5.shutdown() failed")


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    app = JarvisApp()

    app.run()
