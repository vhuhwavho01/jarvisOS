import customtkinter as ctk
from datetime import datetime

from core.jarvis_engine import JarvisEngine
from core.data_manager import DataManager

from ui.chart_widget import ChartWidget
from ui.account_panel import AccountPanel
from ui.trade_panel import TradePanel
from ui.positions_table import PositionsTable
from ui.history_table import HistoryTable


class TradingPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.engine = JarvisEngine()
        self.data = DataManager()

        self.build_ui()

        self.refresh()

    # ==================================================

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="JARVIS AI GOLD TERMINAL",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=10)

        # ================================================
        # TOP
        # ================================================

        top = ctk.CTkFrame(self)
        top.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT SIDE

        left = ctk.CTkFrame(top)
        left.pack(side="left", fill="both", expand=True)

        self.chart = ChartWidget(left)
        self.chart.pack(fill="both", expand=True)

        # RIGHT SIDE

        right = ctk.CTkFrame(top, width=360)
        right.pack(side="right", fill="y", padx=(10, 0))

        self.account = AccountPanel(right)
        self.account.pack(fill="x", padx=10, pady=10)

        self.signal = ctk.CTkLabel(
            right,
            text="WAIT",
            font=("Segoe UI", 34, "bold")
        )

        self.signal.pack(pady=10)

        self.analysis = ctk.CTkTextbox(
            right,
            width=320,
            height=260,
            font=("Consolas", 13)
        )

        self.analysis.pack(fill="x", padx=10)

        self.trade = TradePanel(right)
        self.trade.pack(fill="x", padx=10, pady=10)

        # ================================================
        # OPEN POSITIONS
        # ================================================

        positions_title = ctk.CTkLabel(
            self,
            text="OPEN POSITIONS",
            font=("Segoe UI", 18, "bold")
        )

        positions_title.pack(anchor="w", padx=15)

        self.positions = PositionsTable(self)

        self.positions.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # ================================================
        # HISTORY
        # ================================================

        history_title = ctk.CTkLabel(
            self,
            text="TRADE HISTORY",
            font=("Segoe UI", 18, "bold")
        )

        history_title.pack(anchor="w", padx=15)

        self.history = HistoryTable(self)

        self.history.pack(
            fill="x",
            padx=15,
            pady=(0, 10)
        )

        # ================================================

        self.status = ctk.CTkLabel(
            self,
            text=""
        )

        self.status.pack(pady=5)

    # ==================================================

    def refresh(self):

        df = self.data.get_dataframe()

        if df is not None:
            self.chart.draw(df)

        result = self.engine.analyze_gold()

        if result["status"]:

            colors = {
                "BUY": "lime",
                "SELL": "red",
                "WAIT": "orange"
            }

            self.signal.configure(
                text=result["signal"],
                text_color=colors.get(result["signal"], "white")
            )

            self.analysis.delete("1.0", "end")

            report = f"""
SYMBOL
{result['symbol']}

PRICE
{result['price']}

TREND
{result['trend']}

STRUCTURE
{result['structure']}

CONFIDENCE
{result['confidence']} %

ENTRY
{result['entry']}

STOP LOSS
{result['stop_loss']}

TAKE PROFIT
{result['take_profit']}

RISK REWARD
1:{result['risk_reward']}

----------------------------------

"""

            for reason in result["reasons"]:
                report += f"✓ {reason}\n"

            self.analysis.insert("1.0", report)

        self.status.configure(
            text=f"Updated : {datetime.now().strftime('%H:%M:%S')}"
        )

        self.after(5000, self.refresh)