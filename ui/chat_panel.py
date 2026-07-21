import customtkinter as ctk
from ui.theme import *


class ChatPanel(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=PANEL,
            corner_radius=10
        )

        self.pack(fill="both", expand=True, padx=15, pady=10)

        self.chat = ctk.CTkTextbox(
            self,
            fg_color=PANEL_LIGHT,
            text_color=TEXT,
            font=BODY_FONT
        )

        self.chat.pack(fill="both", expand=True, padx=10, pady=10)

        self.write("🤖 JARVIS OS Started")
        self.write("Type a message below.\n")

    def write(self, message):
        self.chat.insert("end", message + "\n")
        self.chat.see("end")

    def clear(self):
        self.chat.delete("1.0", "end")