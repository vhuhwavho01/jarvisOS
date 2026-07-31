import customtkinter as ctk
from tkinter import ttk
import threading


class OptimizerPage(ctk.CTkFrame):

    def __init__(self, parent, optimizer=None):

        super().__init__(parent)

        self.optimizer = optimizer

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build()

    # ======================================================

    def build(self):

        title = ctk.CTkLabel(

            self,

            text="Strategy Optimizer",

            font=("Segoe UI", 24, "bold")

        )

        title.pack(pady=15)

        top = ctk.CTkFrame(self)

        top.pack(fill="x", padx=15)

        self.run_btn = ctk.CTkButton(

            top,

            text="Run Optimization",

            command=self.run

        )

        self.run_btn.pack(

            side="left",

            padx=10,

            pady=10

        )

        self.progress = ctk.CTkProgressBar(top)

        self.progress.pack(

            side="left",

            fill="x",

            expand=True,

            padx=10

        )

        self.progress.set(0)

        self.status = ctk.CTkLabel(

            self,

            text="Waiting..."

        )

        self.status.pack(pady=10)

        columns = (

            "EMA Fast",

            "EMA Slow",

            "RR",

            "Risk %",

            "Profit",

            "Win Rate",

            "Trades"

        )

        self.table = ttk.Treeview(

            self,

            columns=columns,

            show="headings",

            height=18

        )

        for col in columns:

            self.table.heading(

                col,

                text=col

            )

            self.table.column(

                col,

                width=120,

                anchor="center"

            )

        self.table.pack(

            fill="both",

            expand=True,

            padx=15,

            pady=10

        )

    # ======================================================

    def run(self):

        self.run_btn.configure(

            state="disabled"

        )

        threading.Thread(

            target=self.optimize,

            daemon=True

        ).start()

    # ======================================================

    def optimize(self):

        self.status.configure(

            text="Running optimization..."

        )

        self.progress.set(0.25)

        if self.optimizer is None:

            self.status.configure(

                text="No optimizer connected."

            )

            self.run_btn.configure(

                state="normal"

            )

            self.progress.set(0)

            return

        best = self.optimizer.summary()

        self.progress.set(1.0)

        self.status.configure(

            text="Optimization Complete"

        )

        self.table.delete(

            *self.table.get_children()

        )

        if best:

            self.table.insert(

                "",

                "end",

                values=(

                    best["ema_fast"],

                    best["ema_slow"],

                    best["risk_reward"],

                    best["risk_percent"],

                    round(best["profit"], 2),

                    f"{best['win_rate']:.1f}%",

                    best["trades"]

                )

            )

        self.run_btn.configure(

            state="normal"

        )