import tkinter as tk
from tkinter import Menu

from styles import (
    WIN_BG, WIN_BLACK,
    TITLE_BG_ACTIVE, TITLE_BG_INACTIVE,
    TITLE_FG, FONT_TITLE
)

class WinWindow(tk.Frame):
    active_window = None

    def __init__(self, parent, title, width=300, height=200):
        super().__init__(parent)

        self.parent = parent
        self.on_close = None
        self.is_maximized = False
        self.previous_geometry = None
        self.childs = []

        # создаём внешний фрейм с border
        self.frame = tk.Frame(
            parent,
            bg=WIN_BG,
            highlightbackground=WIN_BLACK,
            highlightthickness=2
        )
        self.frame.place(width=width, height=height)

        # заголовок
        self.title_bar = tk.Frame(self.frame, bg=TITLE_BG_ACTIVE, height=20)
        self.title_bar.pack(fill="x")

        self.title_label = tk.Label(
            self.title_bar, text=title,
            bg=TITLE_BG_ACTIVE, fg=TITLE_FG,
            font=FONT_TITLE, anchor="w"
        )
        self.title_label.pack(side="left", padx=4, fill="x", expand=True)

        # крестик
        self.close_icon = tk.Label(
            self.title_bar, text="☒",
            bg=TITLE_BG_ACTIVE, fg=TITLE_FG,
            font=FONT_TITLE, width=3
        )
        self.close_icon.pack(side="right")
        self.close_icon.bind("<Button-1>", self._show_context_menu)

        # контент
        self.content = tk.Frame(self.frame, bg=WIN_BG)
        self.content.pack(fill="both", expand=True)

        # draggable
        self._make_draggable()

        # corners для ресайза
        self._add_resize_corners()

        # меню (Close, Minimize, Maximize)
        self.context_menu = Menu(self.frame, tearoff=0)
        self.context_menu.add_command(label="Close", command=self._close)
        self.context_menu.add_command(label="Minimize", command=self._minimize)
        self.context_menu.add_command(label="Maximize", command=self._maximize)

        self.activate()

    def activate(self, event=None):
        # снять highlight у предыдущего
        if WinWindow.active_window and WinWindow.active_window.winfo_exists():
            WinWindow.active_window.title_bar.config(bg=TITLE_BG_INACTIVE)
        # сделать active
        self.title_bar.config(bg=TITLE_BG_ACTIVE)
        WinWindow.active_window = self

    def _show_context_menu(self, event=None):
        x = self.close_icon.winfo_rootx()
        y = self.close_icon.winfo_rooty() + self.close_icon.winfo_height()
        self.context_menu.tk_popup(x, y)

    def _close(self):
        if self.on_close: self.on_close()
        self.frame.destroy()

    def _minimize(self):
        if self.is_maximized:
            self._restore()
        else:
            self.previous_geometry = self.frame.place_info()
            self.frame.place_forget()

    def _maximize(self):
        if self.is_maximized:
            return
        self.previous_geometry = self.frame.place_info()
        self.frame.place(x=0, y=0,
                         width=self.parent.winfo_width(),
                         height=self.parent.winfo_height())
        self.is_maximized = True

    def _restore(self):
        geom = self.previous_geometry
        if geom:
            self.frame.place(x=int(geom["x"]), y=int(geom["y"]),
                              width=int(geom["width"]),
                              height=int(geom["height"]))
        self.is_maximized = False

    def _make_draggable(self):
        def start(e):
            self.activate()
            self._drag_x = e.x
            self._drag_y = e.y

        def drag(e):
            x = self.frame.winfo_x() + e.x - self._drag_x
            y = self.frame.winfo_y() + e.y - self._drag_y
            self.frame.place(x=x, y=y)

        self.title_bar.bind("<ButtonPress-1>", start)
        self.title_bar.bind("<B1-Motion>", drag)

    def _add_resize_corners(self):
        # 4 точечных маркера в углах для ресайза
        corners = {}
        for pos in ("nw","ne","se","sw"):
            c = tk.Frame(self.frame, width=10, height=10, bg=WIN_BG, cursor=f"{pos}_corner")
            c.place(**{"nw": {"x":0,"y":0},
                      "ne": {"relx":1.0,"x":0,"y":0,"anchor":"ne"},
                      "se": {"relx":1.0,"rely":1.0,"anchor":"se"},
                      "sw": {"x":0,"rely":1.0,"anchor":"sw"}}[pos])
            corners[pos] = c

        def start(e):
            self._resizing = True
            self._start_x = e.x_root
            self._start_y = e.y_root
            self._orig_w = self.frame.winfo_width()
            self._orig_h = self.frame.winfo_height()

        def resize(e):
            if not getattr(self, "_resizing", False):
                return
            dx = e.x_root - self._start_x
            dy = e.y_root - self._start_y
            neww = max(100, self._orig_w + dx)
            newh = max(80, self._orig_h + dy)
            self.frame.place(width=neww, height=newh)

        for c in corners.values():
            c.bind("<ButtonPress-1>", start)
            c.bind("<B1-Motion>", resize)
