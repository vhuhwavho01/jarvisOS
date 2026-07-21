import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from brain import think


class JarvisGUI:

    def __init__(self):

        self.window = tk.Tk()
        self.window.title("JARVIS OS 2.0")
        self.window.geometry("900x650")
        self.window.configure(bg="#111111")

        # Chat window
        self.chat = ScrolledText(
            self.window,
            bg="#1e1e1e",
            fg="#00ff99",
            font=("Consolas", 11),
            wrap=tk.WORD
        )

        self.chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat.insert(tk.END, "JARVIS OS 2.0 ONLINE\n")
        self.chat.insert(tk.END, "Type 'help' to see built-in commands.\n\n")
        self.chat.config(state=tk.DISABLED)

        # Bottom frame
        bottom = tk.Frame(self.window, bg="#111111")
        bottom.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(
            bottom,
            font=("Consolas", 12)
        )

        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self.send)

        send_btn = tk.Button(
            bottom,
            text="Send",
            command=self.send
        )

        send_btn.pack(side=tk.LEFT, padx=5)

    def write(self, text):

        self.chat.config(state=tk.NORMAL)
        self.chat.insert(tk.END, text + "\n")
        self.chat.see(tk.END)
        self.chat.config(state=tk.DISABLED)

    def send(self, event=None):

        command = self.entry.get().strip()

        if command == "":
            return

        self.write(f"You: {command}")

        self.entry.delete(0, tk.END)

        if command.lower() == "exit":
            self.window.destroy()
            return

        response = think(command)

        if response:
            self.write(f"JARVIS: {response}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    JarvisGUI().run()