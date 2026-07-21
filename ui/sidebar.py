import customtkinter as ctk
from ui.theme import *


class SideBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            width=180,
            fg_color=PANEL,
            corner_radius=0
        )

        self.pack_propagate(False)

        title = ctk.CTkLabel(
            self,
            text="JARVIS",
            font=("Segoe UI", 22, "bold"),
            text_color=ACCENT
        )

        title.pack(pady=(20, 30))

        buttons = [
            "🏠 Home",
            "💬 Chat",
            "🎤 Voice",
            "🧠 Memory",
            "📈 Trading",
            "⚙️ Settings"
        ]

        for name in buttons:

            button = ctk.CTkButton(
                self,
                text=name,
                width=150,
                height=40
            )

            button.pack(pady=6)