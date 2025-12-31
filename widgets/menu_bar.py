import tkinter as tk
from styles import WIN_BG, FONT_NORMAL


class WinMenuBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=WIN_BG, height=20)
        self.pack(fill="x")

    def add_menu(self, title, commands):
        btn = tk.Label(
            self,
            text=title,
            bg=WIN_BG,
            fg="black",
            font=FONT_NORMAL,
            padx=6
        )
        btn.pack(side="left")

        menu = tk.Menu(self, tearoff=0)

        for text, cmd in commands:
            menu.add_command(label=text, command=cmd)

        def popup(e):
            menu.tk_popup(e.x_root, e.y_root)

        btn.bind("<Button-1>", popup)
