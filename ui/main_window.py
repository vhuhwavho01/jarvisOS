import customtkinter as ctk
import threading

from ui.theme import *
from ui.status_bar import StatusBar
from ui.chat_panel import ChatPanel
from ui.toolbar import ToolBar

from core.ai import ask_ai, clear_memory


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("JARVIS OS 2.3")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.configure(fg_color=BACKGROUND)

        self.build_ui()

    def build_ui(self):

        # ===== Title =====
        title = ctk.CTkLabel(
            self,
            text="JARVIS OS",
            font=TITLE_FONT,
            text_color=ACCENT
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Artificial Intelligence Command Center",
            font=BODY_FONT,
            text_color=TEXT_SECONDARY
        )
        subtitle.pack(pady=(0, 10))

        # ===== Status Bar =====
        self.status_bar = StatusBar(self)

        # ===== Chat Panel =====
        self.chat_panel = ChatPanel(self)

        # ===== Toolbar =====
        self.toolbar = ToolBar(
            self,
            send_callback=self.send_message,
            clear_callback=self.clear_chat
        )

    # ===============================
    # SEND MESSAGE
    # ===============================
    def send_message(self):

        message = self.toolbar.get_message().strip()

        if not message:
            return

        self.chat_panel.write(f"🧑 You: {message}")

        self.toolbar.clear_entry()

        self.chat_panel.write("🤖 JARVIS is thinking...")

        threading.Thread(
            target=self.process_ai,
            args=(message,),
            daemon=True
        ).start()

    # ===============================
    # AI THREAD
    # ===============================
    def process_ai(self, message):

        reply = ask_ai(message)

        self.after(0, lambda: self.show_reply(reply))

    # ===============================
    # DISPLAY AI RESPONSE
    # ===============================
    def show_reply(self, reply):

        # Remove the "thinking..." line
        try:
            content = self.chat_panel.chat.get("1.0", "end").splitlines()

            if content and "thinking" in content[-2].lower():
                self.chat_panel.chat.delete("end-2l", "end-1l")
        except:
            pass

        self.chat_panel.write(f"🤖 JARVIS: {reply}")

    # ===============================
    # CLEAR CHAT
    # ===============================
    def clear_chat(self):

        self.chat_panel.clear()

        clear_memory()

        self.chat_panel.write("🤖 Conversation cleared.")