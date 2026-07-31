import customtkinter as ctk

from ui.pages.home_page import HomePage
from ui.pages.chat_page import ChatPage
from ui.pages.voice_page import VoicePage
from ui.pages.memory_page import MemoryPage
from ui.pages.trading_page import TradingPage
from ui.pages.settings_page import SettingsPage


class PageManager:

    def __init__(self, parent):

        self.parent = parent

        self.pages = {

            "home": HomePage(parent),

            "chat": ChatPage(parent),

            "voice": VoicePage(parent),

            "memory": MemoryPage(parent),

            "trading": TradingPage(parent),

            "settings": SettingsPage(parent)

        }

        for page in self.pages.values():

            page.place(
                relx=0,
                rely=0,
                relwidth=1,
                relheight=1
            )

        self.show("home")

    def show(self, name):

        self.pages[name].tkraise()