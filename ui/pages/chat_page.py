import customtkinter as ctk


class ChatPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        label = ctk.CTkLabel(
            self,
            text="Chat Page",
            font=("Arial", 28, "bold")
        )

        label.pack(expand=True)