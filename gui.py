import sys
from datetime import datetime

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QPushButton,
)

from brain import think
from commands import execute
from voice import speak


class JarvisWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("JARVIS OS v0.5")
        self.resize(800, 600)

        self.setStyleSheet("""
            QWidget{
                background:#111827;
                color:white;
                font-size:12pt;
            }

            QTextEdit{
                background:#1f2937;
                border:2px solid #3b82f6;
                border-radius:8px;
            }

            QLineEdit{
                background:#1f2937;
                border:2px solid #3b82f6;
                border-radius:8px;
                padding:8px;
            }

            QPushButton{
                background:#2563eb;
                border-radius:8px;
                padding:8px;
                color:white;
            }

            QPushButton:hover{
                background:#3b82f6;
            }
        """)

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.status = QLabel("🟢 ONLINE")

        self.clock = QLabel()

        top.addWidget(self.status)
        top.addStretch()
        top.addWidget(self.clock)

        layout.addLayout(top)

        self.chat = QTextEdit()
        self.chat.setReadOnly(True)

        layout.addWidget(self.chat)

        bottom = QHBoxLayout()

        self.command = QLineEdit()
        self.command.setPlaceholderText("Enter a command...")

        self.button = QPushButton("Send")

        bottom.addWidget(self.command)
        bottom.addWidget(self.button)

        layout.addLayout(bottom)

        self.setLayout(layout)

        self.chat.append("JARVIS: Welcome to JARVIS OS.")
        self.chat.append("JARVIS: All systems online.\n")

        self.button.clicked.connect(self.process_command)
        self.command.returnPressed.connect(self.process_command)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)

        self.update_clock()

    def update_clock(self):
        now = datetime.now()
        self.clock.setText(now.strftime("%H:%M:%S"))

    def process_command(self):

        command = self.command.text().strip().lower()

        if not command:
            return

        self.chat.append(f"You: {command}")

        self.command.clear()

        if command == "exit":
            speak("Goodbye.")
            self.close()
            return

        if execute(command):
            response = f"Opening {command}..."
            self.chat.append(f"JARVIS: {response}")
            speak(response)
            return

        response = think(command)

        self.chat.append(f"JARVIS: {response}")

        speak(response)


app = QApplication(sys.argv)

window = JarvisWindow()
window.show()

sys.exit(app.exec())