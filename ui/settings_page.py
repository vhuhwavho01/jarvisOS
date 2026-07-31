import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.grid_columnconfigure(0, weight=1)

        self.build()

    # ======================================================

    def build(self):

        title = ctk.CTkLabel(

            self,

            text="JARVIS Settings",

            font=("Segoe UI", 24, "bold")

        )

        title.pack(pady=20)

        # =======================================
        # Trading
        # =======================================

        trading = ctk.CTkFrame(self)

        trading.pack(

            fill="x",

            padx=20,

            pady=10

        )

        ctk.CTkLabel(

            trading,

            text="Trading",

            font=("Segoe UI", 18, "bold")

        ).pack(pady=10)

        ctk.CTkLabel(trading, text="Risk %").pack()

        self.risk = ctk.CTkEntry(trading)

        self.risk.insert(0, "1")

        self.risk.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(trading, text="Risk Reward").pack()

        self.rr = ctk.CTkEntry(trading)

        self.rr.insert(0, "2")

        self.rr.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(trading, text="Minimum Confidence").pack()

        self.confidence = ctk.CTkSlider(

            trading,

            from_=50,

            to=100,

            number_of_steps=50

        )

        self.confidence.set(80)

        self.confidence.pack(

            fill="x",

            padx=20,

            pady=10

        )

        # =======================================
        # Auto Trading
        # =======================================

        auto = ctk.CTkFrame(self)

        auto.pack(

            fill="x",

            padx=20,

            pady=10

        )

        ctk.CTkLabel(

            auto,

            text="Automation",

            font=("Segoe UI", 18, "bold")

        ).pack(pady=10)

        self.auto_trade = ctk.CTkSwitch(

            auto,

            text="Enable Auto Trading"

        )

        self.auto_trade.pack(pady=5)

        self.trailing = ctk.CTkSwitch(

            auto,

            text="Trailing Stop"

        )

        self.trailing.pack(pady=5)

        self.break_even = ctk.CTkSwitch(

            auto,

            text="Break Even"

        )

        self.break_even.pack(pady=5)

        # =======================================
        # Notifications
        # =======================================

        notify = ctk.CTkFrame(self)

        notify.pack(

            fill="x",

            padx=20,

            pady=10

        )

        ctk.CTkLabel(

            notify,

            text="Notifications",

            font=("Segoe UI", 18, "bold")

        ).pack(pady=10)

        self.telegram = ctk.CTkSwitch(

            notify,

            text="Telegram"

        )

        self.telegram.pack(pady=5)

        self.discord = ctk.CTkSwitch(

            notify,

            text="Discord"

        )

        self.discord.pack(pady=5)

        # =======================================
        # Save
        # =======================================

        self.save_button = ctk.CTkButton(

            self,

            text="Save Settings"

        )

        self.save_button.pack(

            pady=20
        )

    # ======================================================

    def values(self):

        return {

            "risk_percent": float(self.risk.get()),

            "risk_reward": float(self.rr.get()),

            "minimum_confidence": int(self.confidence.get()),

            "auto_trade": self.auto_trade.get(),

            "trailing_stop": self.trailing.get(),

            "break_even": self.break_even.get(),

            "telegram": self.telegram.get(),

            "discord": self.discord.get()

        }