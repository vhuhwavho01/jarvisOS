import customtkinter as ctk
import platform
import os

from ui.theme import *


class HomePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color=BACKGROUND)

        self.build_ui()

    def build_ui(self):

        # ==========================
        # Title
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="🏠 Home",
            font=("Segoe UI", 28, "bold"),
            text_color=ACCENT
        )

        title.pack(anchor="w", padx=20, pady=(20, 10))

        # ==========================
        # System Information
        # ==========================

        info_frame = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            corner_radius=12
        )

        info_frame.pack(fill="x", padx=20, pady=10)

        system = platform.system()
        release = platform.release()
        machine = platform.machine()
        python_version = platform.python_version()

        info = [
            ("🤖 JARVIS Version", "4.0"),
            ("🧠 AI Model", "TinyLlama"),
            ("🎤 Voice", "Enabled"),
            ("💾 Memory", "Enabled"),
            ("💻 Operating System", f"{system} {release}"),
            ("⚙ Architecture", machine),
            ("🐍 Python", python_version),
        ]

        for label, value in info:

            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=6)

            left = ctk.CTkLabel(
                row,
                text=label,
                width=220,
                anchor="w",
                font=("Segoe UI", 14, "bold")
            )

            left.pack(side="left")

            right = ctk.CTkLabel(
                row,
                text=value,
                anchor="w",
                font=("Segoe UI", 14)
            )

            right.pack(side="left")

        # ==========================
        # Quick Actions
        # ==========================

        actions = ctk.CTkFrame(
            self,
            fg_color=PANEL,
            corner_radius=12
        )

        actions.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(
            actions,
            text="⚡ Quick Actions",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", padx=15, pady=(15, 10))

        buttons = ctk.CTkFrame(actions, fg_color="transparent")
        buttons.pack(fill="x", padx=15, pady=(0, 15))

        ctk.CTkButton(
            buttons,
            text="Open TradingView",
            width=180
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Open Notepad",
            width=180
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons,
            text="Open Calculator",
            width=180
        ).pack(side="left", padx=5)