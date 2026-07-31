import customtkinter as ctk


class VoicePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Voice",
            font=("Arial", 28, "bold")
        ).pack(expand=True)