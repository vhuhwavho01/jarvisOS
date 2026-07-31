import customtkinter as ctk


class HomePage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Home",
            font=("Arial", 28, "bold")
        ).pack(expand=True)