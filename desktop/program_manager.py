import tkinter as tk
from widgets.menu_bar import WinMenuBar
from widgets.program_icon import ProgramIcon


class ProgramManagerContent(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=parent["bg"])
        self.app = app

        self._create_menu()
        self._create_icons()

    def _create_menu(self):
        self.menu = WinMenuBar(self)
        self.menu.pack(fill="x")


        self.menu.add_menu("Run", [
            ("Notepad", self.app.open_notepad),
            ("Calculator", self.app.open_calc)
        ])

    def _create_icons(self):
        icons = tk.Frame(self, bg=self["bg"])
        icons.pack(fill="both", expand=True, padx=12, pady=12)

        ProgramIcon(
            icons,
            "Notepad",
            self.app.open_notepad,
            image_path="icons/notepad.png",
        ).grid(row=0, column=0, padx=12, pady=12)

        ProgramIcon(
            icons,
            "Calculator",
            self.app.open_calc,
            image_path="icons/calculator.png",
        ).grid(row=0, column=1, padx=12, pady=12)
