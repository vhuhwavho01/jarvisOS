import os
import subprocess
import webbrowser


def execute(command):

    cmd = command.lower()

    # ==========================
    # Chrome
    # ==========================

    if "open chrome" in cmd:
        os.system("start chrome")
        return "Opening Google Chrome."

    # ==========================
    # Notepad
    # ==========================

    if "open notepad" in cmd:
        subprocess.Popen("notepad")
        return "Opening Notepad."

    # ==========================
    # Calculator
    # ==========================

    if "open calculator" in cmd:
        subprocess.Popen("calc")
        return "Opening Calculator."

    # ==========================
    # TradingView
    # ==========================

    if "open tradingview" in cmd:
        webbrowser.open("https://www.tradingview.com")
        return "Opening TradingView."

    return None