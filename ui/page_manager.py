import customtkinter as ctk

from ui.pages.home_page import HomePage


class PageManager(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.pack(fill="both", expand=True)

        self.current_page = None

        self.show_home()

    # ===================================
    # Remove Current Page
    # ===================================

    def clear_page(self):

        if self.current_page is not None:
            self.current_page.destroy()

    # ===================================
    # HOME
    # ===================================

    def show_home(self):

        self.clear_page()

        self.current_page = HomePage(self)

        self.current_page.pack(fill="both", expand=True)