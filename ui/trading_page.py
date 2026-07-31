import customtkinter as ctk
from tkinter import ttk

from ui.trade_panel import TradePanel
from ui.chart_widget import ChartWidget


class TradingPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        # ==============================
        # Chart
        # ==============================

        self.chart = ChartWidget(self)

        self.chart.grid(

            row=0,

            column=0,

            sticky="nsew",

            padx=10,

            pady=10

        )

        # ==============================
        # Right Side
        # ==============================

        right = ctk.CTkFrame(self)

        right.grid(

            row=0,

            column=1,

            sticky="nsew",

            padx=10,

            pady=10

        )

        right.grid_rowconfigure(1, weight=1)

        self.trade_panel = TradePanel(right)

        self.trade_panel.pack(

            fill="x",

            padx=5,

            pady=5

        )

        self.signal = ctk.CTkLabel(

            right,

            text="WAIT",

            font=("Segoe UI", 22, "bold")

        )

        self.signal.pack(pady=10)

        columns = (

            "Ticket",

            "Symbol",

            "Type",

            "Volume",

            "Profit"

        )

        self.positions = ttk.Treeview(

            right,

            columns=columns,

            show="headings",

            height=10

        )

        for col in columns:

            self.positions.heading(col, text=col)

            self.positions.column(

                col,

                width=90,

                anchor="center"

            )

        self.positions.pack(

            fill="both",

            expand=True,

            padx=5,

            pady=5

        )

    # =====================================================

    def update_signal(self, result):

        signal = result.get("signal", "WAIT")

        confidence = result.get("confidence", 0)

        self.signal.configure(

            text=f"{signal} ({confidence}%)"

        )

    # =====================================================

    def load_positions(self, positions):

        self.positions.delete(

            *self.positions.get_children()

        )

        for pos in positions:

            self.positions.insert(

                "",

                "end",

                values=(

                    pos.ticket,

                    pos.symbol,

                    "BUY" if pos.type == 0 else "SELL",

                    pos.volume,

                    round(pos.profit, 2)

                )

            )