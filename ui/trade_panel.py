import customtkinter as ctk

from core.trade_manager import TradeManager
from core.auto_trader import AutoTrader


class TradePanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.trade_manager = TradeManager()

        self.auto_trader = AutoTrader()

        self.build()

    # =====================================================

    def build(self):

        ctk.CTkLabel(

            self,

            text="TRADE PANEL",

            font=("Segoe UI", 22, "bold")

        ).pack(pady=20)

        # ------------------------------------

        ctk.CTkLabel(

            self,

            text="Symbol"

        ).pack()

        self.symbol = ctk.CTkComboBox(

            self,

            values=[

                "XAUUSD",

                "EURUSD",

                "GBPUSD",

                "USDJPY",

                "BTCUSD"

            ]

        )

        self.symbol.set("XAUUSD")

        self.symbol.pack(

            fill="x",

            padx=20,

            pady=5

        )

        # ------------------------------------

        ctk.CTkLabel(

            self,

            text="Lot Size"

        ).pack()

        self.lot = ctk.CTkEntry(self)

        self.lot.insert(

            0,

            "0.01"

        )

        self.lot.pack(

            fill="x",

            padx=20,

            pady=5

        )

        # ------------------------------------

        self.buy = ctk.CTkButton(

            self,

            text="BUY",

            fg_color="green",

            command=self.buy_order

        )

        self.buy.pack(

            fill="x",

            padx=20,

            pady=5

        )

        self.sell = ctk.CTkButton(

            self,

            text="SELL",

            fg_color="red",

            command=self.sell_order

        )

        self.sell.pack(

            fill="x",

            padx=20,

            pady=5

        )

        self.close = ctk.CTkButton(

            self,

            text="CLOSE ALL",

            command=self.close_all

        )

        self.close.pack(

            fill="x",

            padx=20,

            pady=5

        )

        # ------------------------------------

        self.auto = ctk.CTkSwitch(

            self,

            text="Auto Trade",

            command=self.toggle_auto

        )

        self.auto.pack(

            pady=20

        )

        # ------------------------------------

        self.status = ctk.CTkLabel(

            self,

            text="READY",

            font=("Segoe UI", 18)

        )

        self.status.pack(

            pady=10

        )

    # =====================================================

    def symbol_name(self):

        return self.symbol.get()

    # =====================================================

    def lot_size(self):

        try:

            return float(self.lot.get())

        except:

            return 0.01

    # =====================================================

    def buy_order(self):

        self.trade_manager.buy(

            self.symbol_name(),

            self.lot_size(),

            0,

            0

        )

        self.status.configure(

            text="BUY SENT"

        )

    # =====================================================

    def sell_order(self):

        self.trade_manager.sell(

            self.symbol_name(),

            self.lot_size(),

            0,

            0

        )

        self.status.configure(

            text="SELL SENT"

        )

    # =====================================================

    def close_all(self):

        self.trade_manager.close_all()

        self.status.configure(

            text="ALL CLOSED"

        )

    # =====================================================

    def toggle_auto(self):

        if self.auto.get():

            self.auto_trader.set_symbol(

                self.symbol_name()

            )

            self.auto_trader.set_lot(

                self.lot_size()

            )

            self.auto_trader.start()

            self.status.configure(

                text="AUTO TRADING"

            )

        else:

            self.auto_trader.stop()

            self.status.configure(

                text="AUTO STOPPED"
            )