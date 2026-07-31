import customtkinter as ctk
from tkinter import ttk


class PerformancePage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)

        self.cards = {}

        self.create_summary()
        self.create_trade_table()

    # ======================================================

    def create_summary(self):

        items = [

            "Balance",
            "Equity",
            "Profit",
            "Win Rate",
            "Trades",
            "Profit Factor",
            "Drawdown",
            "AI Accuracy"

        ]

        for i, title in enumerate(items):

            frame = ctk.CTkFrame(self)

            frame.grid(

                row=i // 4,

                column=i % 4,

                padx=10,

                pady=10,

                sticky="nsew"

            )

            ctk.CTkLabel(

                frame,

                text=title,

                font=("Segoe UI", 15, "bold")

            ).pack(pady=(12, 5))

            value = ctk.CTkLabel(

                frame,

                text="--",

                font=("Segoe UI", 22)

            )

            value.pack(pady=(5, 12))

            self.cards[title] = value

    # ======================================================

    def create_trade_table(self):

        frame = ctk.CTkFrame(self)

        frame.grid(

            row=2,

            column=0,

            columnspan=4,

            sticky="nsew",

            padx=10,

            pady=10

        )

        columns = (

            "Ticket",

            "Symbol",

            "Type",

            "Entry",

            "Exit",

            "Profit",

            "Confidence"

        )

        self.table = ttk.Treeview(

            frame,

            columns=columns,

            show="headings",

            height=12

        )

        for col in columns:

            self.table.heading(col, text=col)

            self.table.column(

                col,

                width=110,

                anchor="center"

            )

        self.table.pack(

            fill="both",

            expand=True

        )

    # ======================================================

    def update_summary(self, stats):

        self.cards["Balance"].configure(

            text=f"{stats.get('balance',0):.2f}"

        )

        self.cards["Equity"].configure(

            text=f"{stats.get('equity',0):.2f}"

        )

        self.cards["Profit"].configure(

            text=f"{stats.get('profit',0):.2f}"

        )

        self.cards["Win Rate"].configure(

            text=f"{stats.get('win_rate',0):.1f}%"

        )

        self.cards["Trades"].configure(

            text=str(stats.get("trades", 0))

        )

        self.cards["Profit Factor"].configure(

            text=f"{stats.get('profit_factor',0):.2f}"

        )

        self.cards["Drawdown"].configure(

            text=f"{stats.get('drawdown',0):.2f}%"

        )

        self.cards["AI Accuracy"].configure(

            text=f"{stats.get('accuracy',0):.1f}%"

        )

    # ======================================================

    def load_history(self, trades):

        self.table.delete(

            *self.table.get_children()

        )

        for trade in trades:

            self.table.insert(

                "",

                "end",

                values=trade

            )