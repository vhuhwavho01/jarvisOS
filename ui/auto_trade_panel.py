import customtkinter as ctk

from core.auto_trader import AutoTrader


class AutoTradePanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.auto = AutoTrader()

        self.build()

    # =====================================================

    def build(self):

        title = ctk.CTkLabel(

            self,

            text="AUTO TRADER",

            font=("Segoe UI", 18, "bold")

        )

        title.pack(pady=(10,5))

        # =========================================

        ctk.CTkLabel(

            self,

            text="Lot Size"

        ).pack()

        self.volume = ctk.CTkEntry(

            self,

            width=140

        )

        self.volume.insert(0, "0.01")

        self.volume.pack(pady=5)

        # =========================================

        ctk.CTkLabel(

            self,

            text="Minimum Confidence"

        ).pack()

        self.confidence = ctk.CTkEntry(

            self,

            width=140

        )

        self.confidence.insert(0, "80")

        self.confidence.pack(pady=5)

        # =========================================

        ctk.CTkLabel(

            self,

            text="Scan Interval (seconds)"

        ).pack()

        self.interval = ctk.CTkEntry(

            self,

            width=140

        )

        self.interval.insert(0, "60")

        self.interval.pack(pady=5)

        # =========================================

        self.status = ctk.CTkLabel(

            self,

            text="STOPPED",

            text_color="red",

            font=("Segoe UI", 15, "bold")

        )

        self.status.pack(pady=10)

        # =========================================

        self.start_btn = ctk.CTkButton(

            self,

            text="START AUTO TRADING",

            fg_color="green",

            command=self.start

        )

        self.start_btn.pack(

            fill="x",

            padx=15,

            pady=5

        )

        self.stop_btn = ctk.CTkButton(

            self,

            text="STOP",

            fg_color="red",

            command=self.stop

        )

        self.stop_btn.pack(

            fill="x",

            padx=15,

            pady=(0,10)

        )

    # =====================================================

    def start(self):

        try:

            self.auto.set_volume(

                float(self.volume.get())

            )

            self.auto.set_confidence(

                int(self.confidence.get())

            )

            self.auto.set_interval(

                int(self.interval.get())

            )

            self.auto.start()

            self.status.configure(

                text="RUNNING",

                text_color="lime"

            )

        except Exception as e:

            self.status.configure(

                text=str(e),

                text_color="red"

            )

    # =====================================================

    def stop(self):

        self.auto.stop()

        self.status.configure(

            text="STOPPED",

            text_color="red"

        )