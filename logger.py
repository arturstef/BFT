import tkinter as tk
from tkinter import SW


class Logger:
    lines = []

    def __init__(self, master, max_messages=10, width=3, height=100):
        self.master = master
        self.max_messages = max_messages
        self.master.config(width=width, height=height)

        self.message_text = tk.Text(master, wrap="word", state=tk.DISABLED, width=width)
        self.message_text.grid(row=1, column=0, padx=10, pady=10, sticky=SW)

    def new_message(self, message):
        if message:
            self.message_text.config(state=tk.NORMAL)
            self.lines.append(message)
            if len(self.lines) > self.max_messages:
                self.lines.pop(0)
            new_content = "\n".join(list(reversed(self.lines)))
            self.message_text.delete("1.0", tk.END)
            self.message_text.insert(tk.END, new_content)
            self.message_text.config(state=tk.DISABLED)