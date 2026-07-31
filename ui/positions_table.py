import customtkinter as ctk
import MetaTrader5 as mt5


class PositionsTable(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.headers = [
            "Ticket",
            "Symbol",
            "Type",
            "Volume",
            "Open",
            "Current",
            "Profit"
        ]

        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.pack(fill="x")

        for i, title in enumerate(self.headers):

            lbl = ctk.CTkLabel(
                self.header_frame,
                text=title,
                width=110,
                font=("Segoe UI", 13, "bold")
            )

            lbl.grid(row=0, column=i, padx=2, pady=5)

        self.table = ctk.CTkScrollableFrame(
            self,
            height=180
        )

        self.table.pack(
            fill="both",
            expand=True
        )

        self.refresh()

    # ======================================================

    def refresh(self):

        for widget in self.table.winfo_children():
            widget.destroy()

        positions = mt5.positions_get()

        if positions is None:
            positions = []

        for r, pos in enumerate(positions):

            tick = mt5.symbol_info_tick(pos.symbol)

            if tick:

                current = (
                    tick.bid
                    if pos.type == mt5.POSITION_TYPE_BUY
                    else tick.ask
                )

            else:

                current = 0

            values = [

                pos.ticket,

                pos.symbol,

                "BUY"
                if pos.type == mt5.POSITION_TYPE_BUY
                else "SELL",

                f"{pos.volume:.2f}",

                f"{pos.price_open:.2f}",

                f"{current:.2f}",

                f"{pos.profit:.2f}"

            ]

            for c, value in enumerate(values):

                color = "white"

                if c == 2:

                    color = (
                        "lime"
                        if value == "BUY"
                        else "red"
                    )

                if c == 6:

                    color = (
                        "lime"
                        if pos.profit >= 0
                        else "red"
                    )

                lbl = ctk.CTkLabel(

                    self.table,

                    text=value,

                    width=110,

                    text_color=color

                )

                lbl.grid(
                    row=r,
                    column=c,
                    padx=2,
                    pady=2
                )

        self.after(
            3000,
            self.refresh
        )