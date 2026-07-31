import customtkinter as ctk


class DashboardPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)

        self.cards = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1, 2), weight=1)

        self.build_dashboard()

    # =====================================================

    def build_dashboard(self):

        title = ctk.CTkLabel(
            self,
            text="JARVIS AI Dashboard",
            font=("Segoe UI", 28, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=3,
            pady=(20, 30)
        )

        card_names = [

            "Signal",
            "Confidence",
            "AI Score",

            "Trend",
            "Market Regime",
            "Session",

            "News",
            "Trade Status",
            "Risk Reward",

            "Entry",
            "Stop Loss",
            "Take Profit"

        ]

        row = 1
        col = 0

        for name in card_names:

            card = self.create_card(name)

            card.grid(
                row=row,
                column=col,
                padx=15,
                pady=15,
                sticky="nsew"
            )

            col += 1

            if col == 3:

                col = 0
                row += 1
                    # =====================================================

    def create_card(self, title):

        frame = ctk.CTkFrame(
            self,
            corner_radius=12
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14)
        )

        label.pack(
            pady=(12, 4)
        )

        value = ctk.CTkLabel(
            frame,
            text="--",
            font=("Segoe UI", 22, "bold")
        )

        value.pack(
            pady=(0, 15)
        )

        self.cards[title] = value

        return frame