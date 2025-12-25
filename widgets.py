import tkinter as tk
from styles import WIN_BG, WIN_DARK, WIN_BLACK, TITLE_BG_ACTIVE, TITLE_FG, FONT_NORMAL, FONT_TITLE

class WinButton(tk.Frame):
    def __init__(self, parent, text, command=None, width=80, height=25):
        super().__init__(parent, bg=WIN_BG, width=width, height=height, highlightbackground=WIN_BLACK, highlightthickness=1)
        self.command = command
        self.label = tk.Label(self, text=text, bg=WIN_BG, fg="black", font=FONT_NORMAL)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.bind("<Button-1>", self.click)
        self.label.bind("<Button-1>", self.click)
        self.bind("<ButtonPress-1>", self.press)
        self.bind("<ButtonRelease-1>", self.release)
        self.label.bind("<ButtonPress-1>", self.press)
        self.label.bind("<ButtonRelease-1>", self.release)

    def press(self, event):
        self.config(bg=WIN_DARK)
        self.label.config(bg=WIN_DARK)

    def release(self, event):
        self.config(bg=WIN_BG)
        self.label.config(bg=WIN_BG)
        if self.command:
            self.command()

    def click(self, event):
        pass


class WinWindow(tk.Frame):
    def __init__(self, parent, title, width=300, height=200):
        super().__init__(parent, bg=WIN_BG, width=width, height=height, highlightbackground=WIN_BLACK, highlightthickness=2)
        self.pack_propagate(False)

        # Заголовок
        self.title_bar = tk.Frame(self, bg=TITLE_BG_ACTIVE, height=22)
        self.title_bar.pack(fill="x")
        self.title_label = tk.Label(
            self.title_bar,
            text=title,
            bg=TITLE_BG_ACTIVE,
            fg=TITLE_FG,
            font=FONT_TITLE,
            anchor="w",
            padx=5
        )
        self.title_label.pack(fill="both")

        # Контент
        self.content = tk.Frame(self, bg=WIN_BG)
        self.content.pack(fill="both", expand=True)
