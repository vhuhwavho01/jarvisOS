import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Settings",
            font=("Arial", 28, "bold")
        ).pack(expand=True)