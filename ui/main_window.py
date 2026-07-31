import customtkinter as ctk

from ui.dashboard_page import DashboardPage
from ui.trading_page import TradingPage
from ui.performance_page import PerformancePage
from ui.optimizer_page import OptimizerPage
from ui.settings_page import SettingsPage


class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("JARVIS AI Trading Terminal")

        self.geometry("1700x950")

        self.minsize(1500, 850)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()

        self.create_pages()

    # ======================================================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(

            self,

            width=220,

            corner_radius=0

        )

        self.sidebar.grid(

            row=0,

            column=0,

            sticky="ns"

        )

        self.sidebar.grid_propagate(False)

        title = ctk.CTkLabel(

            self.sidebar,

            text="JARVIS",

            font=("Segoe UI", 28, "bold")

        )

        title.pack(

            pady=(30, 5)

        )

        subtitle = ctk.CTkLabel(

            self.sidebar,

            text="AI Trading Terminal"

        )

        subtitle.pack(

            pady=(0, 30)

        )

        buttons = [

            ("Dashboard", self.show_dashboard),

            ("Trading", self.show_trading),

            ("Performance", self.show_performance),

            ("Optimizer", self.show_optimizer),

            ("Settings", self.show_settings)

        ]

        for text, command in buttons:

            ctk.CTkButton(

                self.sidebar,

                text=text,

                command=command

            ).pack(

                fill="x",

                padx=15,

                pady=5

            )

    # ======================================================

    def create_pages(self):

        self.container = ctk.CTkFrame(

            self,

            fg_color="transparent"

        )

        self.container.grid(

            row=0,

            column=1,

            sticky="nsew"

        )

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.dashboard = DashboardPage(self.container)
        self.trading = TradingPage(self.container)
        self.performance = PerformancePage(self.container)
        self.optimizer = OptimizerPage(self.container)
        self.settings = SettingsPage(self.container)

        self.pages = [

            self.dashboard,
            self.trading,
            self.performance,
            self.optimizer,
            self.settings

        ]

        for page in self.pages:

            page.grid(

                row=0,

                column=0,

                sticky="nsew"

            )

        self.dashboard.tkraise()

    # ======================================================

    def show_dashboard(self):

        self.dashboard.tkraise()

    def show_trading(self):

        self.trading.tkraise()

    def show_performance(self):

        self.performance.tkraise()

    def show_optimizer(self):

        self.optimizer.tkraise()

    def show_settings(self):

        self.settings.tkraise()