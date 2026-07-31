import customtkinter as ctk


class MemoryPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Memory",
            font=("Arial", 28, "bold")
        ).pack(expand=True)