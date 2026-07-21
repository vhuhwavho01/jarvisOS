import customtkinter as ctk
import threading

from ui.theme import *
from ui.sidebar import SideBar
from ui.status_bar import StatusBar
from ui.chat_panel import ChatPanel
from ui.toolbar import ToolBar

from core.brain import Brain
from core.ai import clear_memory
from core.voice import speak, listen


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JARVIS OS v3.1")
        self.geometry("1400x850")
        self.minsize(1200, 700)

        self.configure(fg_color=BACKGROUND)

        self.brain = Brain()

        self.build_ui()

    # ==========================================
    # BUILD UI
    # ==========================================

    def build_ui(self):

        # Main container
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND
        )
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = SideBar(self.main_frame)
        self.sidebar.pack(side="left", fill="y")

        # Right side
        self.content = ctk.CTkFrame(
            self.main_frame,
            fg_color=BACKGROUND
        )
        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        # Header
        title = ctk.CTkLabel(
            self.content,
            text="JARVIS OS",
            font=TITLE_FONT,
            text_color=ACCENT
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self.content,
            text="Artificial Intelligence Command Center",
            font=BODY_FONT,
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(pady=(0, 10))

        # Status bar
        self.status = StatusBar(self.content)

        # Chat panel
        self.chat_panel = ChatPanel(self.content)

        # Toolbar
        self.toolbar = ToolBar(
            self.content,
            send_callback=self.send_message,
            clear_callback=self.clear_chat,
            mic_callback=self.start_voice
        )

    # ==========================================
    # SEND MESSAGE
    # ==========================================

    def send_message(self):

        message = self.toolbar.get_message().strip()

        if not message:
            return

        self.chat_panel.write(f"🧑 You: {message}")

        self.toolbar.clear_entry()

        threading.Thread(
            target=self.process_message,
            args=(message,),
            daemon=True
        ).start()

    # ==========================================
    # PROCESS MESSAGE
    # ==========================================

    def process_message(self, message):

        self.after(
            0,
            lambda: self.chat_panel.write("🤖 JARVIS is thinking...")
        )

        reply = self.brain.process(message)

        self.after(
            0,
            lambda: self.display_reply(reply)
        )

    # ==========================================
    # DISPLAY REPLY
    # ==========================================

    def display_reply(self, reply):

        self.chat_panel.write(f"🤖 JARVIS: {reply}")

        speak(reply)

    # ==========================================
    # VOICE INPUT
    # ==========================================

    def start_voice(self):

        threading.Thread(
            target=self.voice_thread,
            daemon=True
        ).start()

    def voice_thread(self):

        self.after(
            0,
            lambda: self.chat_panel.write("🎤 Listening...")
        )

        try:

            text = listen()

            if text:

                self.after(
                    0,
                    lambda: self.toolbar.set_message(text)
                )

                self.after(
                    100,
                    self.send_message
                )

        except Exception as e:

            self.after(
                0,
                lambda: self.chat_panel.write(f"❌ Voice Error: {e}")
            )

    # ==========================================
    # CLEAR CHAT
    # ==========================================

    def clear_chat(self):

        self.chat_panel.clear()

        clear_memory()

        self.chat_panel.write("🤖 Conversation cleared.")