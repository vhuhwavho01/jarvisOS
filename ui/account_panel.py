import customtkinter as ctk
import MetaTrader5 as mt5


class AccountPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master, corner_radius=10)

        self.build_ui()

        self.refresh()

    # ======================================================

    def build_ui(self):

        ctk.CTkLabel(

            self,

            text="ACCOUNT",

            font=("Segoe UI", 20, "bold")

        ).pack(pady=(15, 20))

        self.login = self.create_item("Login")
        self.server = self.create_item("Server")
        self.balance = self.create_item("Balance")
        self.equity = self.create_item("Equity")
        self.margin = self.create_item("Margin")
        self.free_margin = self.create_item("Free Margin")
        self.profit = self.create_item("Floating P/L")
        self.leverage = self.create_item("Leverage")

    # ======================================================

    def create_item(self, title):

        frame = ctk.CTkFrame(self)

        frame.pack(

            fill="x",

            padx=10,

            pady=4

        )

        ctk.CTkLabel(

            frame,

            text=title,

            anchor="w",

            width=120

        ).pack(

            side="left",

            padx=10

        )

        value = ctk.CTkLabel(

            frame,

            text="--"

        )

        value.pack(

            side="right",

            padx=10

        )

        return value

    # ======================================================

    def refresh(self):

        info = mt5.account_info()

        if info is None:

            self.after(

                5000,

                self.refresh

            )

            return

        self.login.configure(

            text=str(info.login)

        )

        self.server.configure(

            text=info.server

        )

        self.balance.configure(

            text=f"{info.balance:.2f}"

        )

        self.equity.configure(

            text=f"{info.equity:.2f}"

        )

        self.margin.configure(

            text=f"{info.margin:.2f}"

        )

        self.free_margin.configure(

            text=f"{info.margin_free:.2f}"

        )

        self.profit.configure(

            text=f"{info.profit:.2f}"

        )

        self.leverage.configure(

            text=f"1:{info.leverage}"

        )

        self.after(

            5000,

            self.refresh

        )