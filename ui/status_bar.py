import customtkinter as ctk
import psutil
from datetime import datetime

from ui.theme import *


class StatusBar(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(
            master,
            fg_color=PANEL,
            corner_radius=10,
            height=60
        )

        self.pack(fill="x", padx=15, pady=10)

        # Online Status
        self.status = ctk.CTkLabel(
            self,
            text="🟢 ONLINE",
            font=BUTTON_FONT,
            text_color=SUCCESS
        )

        self.status.pack(side="left", padx=15)

        # AI Model
        self.model = ctk.CTkLabel(
            self,
            text="MODEL: TinyLlama",
            font=BODY_FONT,
            text_color=TEXT
        )

        self.model.pack(side="left", padx=20)

        # CPU Usage
        self.cpu = ctk.CTkLabel(
            self,
            text="CPU: 0%",
            font=BODY_FONT
        )

        self.cpu.pack(side="right", padx=20)

        # RAM Usage
        self.ram = ctk.CTkLabel(
            self,
            text="RAM: 0%",
            font=BODY_FONT
        )

        self.ram.pack(side="right", padx=20)

        # Clock
        self.clock = ctk.CTkLabel(
            self,
            text="00:00:00",
            font=BODY_FONT
        )

        self.clock.pack(side="right", padx=20)

        self.update_status()

    def update_status(self):

        self.cpu.configure(
            text=f"CPU: {psutil.cpu_percent()}%"
        )

        self.ram.configure(
            text=f"RAM: {psutil.virtual_memory().percent}%"
        )

        self.clock.configure(
            text=datetime.now().strftime("%H:%M:%S")
        )

        self.after(1000, self.update_status)