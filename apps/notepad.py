import tkinter as tk
from styles import WIN_BG, WIN_BLACK, WIN_LIGHT, FONT_NORMAL
from widgets.win_button import WinButton


class NotepadContent(tk.Frame):
    def __init__(self, parent, text=""):
        super().__init__(parent, bg=WIN_BG)

        self.text_content = text
        self._create_menu()
        self._create_text_area()
        self._create_status_bar()

    def _create_menu(self):
        menu = tk.Frame(self, bg=WIN_BG, bd=1, relief="raised")
        menu.pack(fill="x")

        WinButton(menu, "File", width=60).pack(side="left", padx=2)
        WinButton(menu, "Edit", width=60).pack(side="left", padx=2)
        WinButton(menu, "Help", width=60).pack(side="left", padx=2)

    def _create_text_area(self):
        frame = tk.Frame(self, bg=WIN_BG, bd=2, relief="sunken")
        frame.pack(fill="both", expand=True, padx=4, pady=4)

        self.text = tk.Text(
            frame,
            font=FONT_NORMAL,
            bg=WIN_LIGHT,
            fg=WIN_BLACK,
            bd=0
        )
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", self.text_content)

    def _create_status_bar(self):
        self.status = tk.Label(
            self,
            text="Ln 1, Col 1",
            bg=WIN_BG,
            fg=WIN_BLACK,
            anchor="w",
            padx=4
        )
        self.status.pack(fill="x")
