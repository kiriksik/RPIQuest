import tkinter as tk
from styles import DESKTOP_BG
from widgets.program_icon import ProgramIcon
from .program_manager import ProgramManagerContent
from widgets.window.manager import WindowManager
from widgets.window.flags import WindowFlags

class Desktop(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=DESKTOP_BG)
        self.app = app

        # 🔹 слой иконок (ниже всех окон)
        self.icon_layer = tk.Frame(self, bg=DESKTOP_BG)
        self.icon_layer.place(x=0, y=0, relwidth=1, relheight=1)
        self._create_desktop_icons()

        # 🔹 слой окон (поверх иконок) — прозрачный
        self.wm_layer = tk.Frame(self)  # фон такой же, как у Desktop
        # self.wm_layer.place(x=0, y=0, relwidth=1, relheight=1)
        self.wm = WindowManager(self)

        self.pm_window = None
        self.restore_program_manager()

    def _create_desktop_icons(self):
        ProgramIcon(
            self.icon_layer,
            "Program Manager",
            self.restore_program_manager,
            image_path = "./icons/program_manager.png",
        ).place(x=20, y=20)

    def restore_program_manager(self):
        if self.pm_window and getattr(self.pm_window, "frame", None):
            self.pm_window.activate()
            return

        self.pm_window = self.wm.create_window(
            title="Program Manager",
            content=lambda parent: ProgramManagerContent(parent, self.app),
            size=(80, 60, 360, 240),
            flags=WindowFlags.WN_DRAGABLE,
        )
        self.pm_window.frame.lift()  # поднимаем само окно поверх других окон
