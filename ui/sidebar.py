import customtkinter as ctk
from ui.theme import *


class SideBar(ctk.CTkFrame):

    def __init__(self, master, page_callback):

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

        pages = [
            ("🏠 Home", "home"),
            ("💬 Chat", "chat"),
            ("🎤 Voice", "voice"),
            ("🧠 Memory", "memory"),
            ("📈 Trading", "trading"),
            ("⚙️ Settings", "settings"),
        ]

        self.buttons = {}

        for text, page in pages:

            btn = ctk.CTkButton(
                self,
                text=text,
                width=150,
                height=40,
                command=lambda p=page: page_callback(p)
            )

            btn.pack(pady=6)

            self.buttons[page] = btn