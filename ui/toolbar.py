import customtkinter as ctk
from ui.theme import *


class ToolBar(ctk.CTkFrame):

    def __init__(self, master, send_callback, clear_callback, mic_callback):

        super().__init__(
            master,
            fg_color=PANEL,
            corner_radius=10
        )

        self.pack(fill="x", padx=15, pady=(0, 15))

        # ==========================
        # Input Box
        # ==========================

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Ask JARVIS anything...",
            font=BODY_FONT
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10,
            pady=10
        )

        self.entry.bind("<Return>", lambda event: send_callback())

        # ==========================
        # Send Button
        # ==========================

        self.send_btn = ctk.CTkButton(
            self,
            text="Send",
            width=90,
            command=send_callback
        )

        self.send_btn.pack(side="left", padx=5)

        # ==========================
        # Microphone Button
        # ==========================

        self.mic_btn = ctk.CTkButton(
            self,
            text="🎤",
            width=50,
            command=mic_callback
        )

        self.mic_btn.pack(side="left", padx=5)

        # ==========================
        # Clear Button
        # ==========================

        self.clear_btn = ctk.CTkButton(
            self,
            text="Clear",
            width=90,
            command=clear_callback
        )

        self.clear_btn.pack(side="left", padx=5)

    # ==========================
    # Get typed message
    # ==========================

    def get_message(self):
        return self.entry.get().strip()

    # ==========================
    # Set message
    # ==========================

    def set_message(self, text):
        self.entry.delete(0, "end")
        self.entry.insert(0, text)

    # ==========================
    # Clear input
    # ==========================

    def clear_entry(self):
        self.entry.delete(0, "end")