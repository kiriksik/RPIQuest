import tkinter as tk
from .flags import WindowFlags


WIN_BG = "#C0C0C0"
TITLE_ACTIVE = "#000080"
TITLE_INACTIVE = "#808080"
TITLE_FG = "#FFFFFF"


class Window:
    active_window = None

    def __init__(self, parent, title, content, size, flags):
        self.is_minimized = False
        self.parent = parent
        self.title = title
        self.flags = flags
        self.content_class = content

        self.is_dragging = False
        self.is_resizing = False
        self.is_maximized = False
        self.childs = []

        x, y, w, h = size
        self.prev_geom = size

        self.frame = tk.Frame(
            parent,
            bg=WIN_BG,
            highlightthickness=2,
            highlightbackground="black"
        )
        self.frame.place(x=x, y=y, width=w, height=h)

        self._create_titlebar()
        self._create_content()
        self._bind_window()

        if content:
            self.set_content(content)

        self.activate()

    # ================= TITLE BAR =================

    def _create_titlebar(self):
        self.titlebar = tk.Frame(
            self.frame,
            bg=TITLE_ACTIVE,
            height=22
        )
        self.titlebar.pack(fill="x")

        self.menu_btn = tk.Label(
            self.titlebar,
            text="≡",
            bg=TITLE_ACTIVE,
            fg=TITLE_FG,
            width=3
        )
        self.menu_btn.pack(side="left")

        self.title_lbl = tk.Label(
            self.titlebar,
            text=self.title,
            bg=TITLE_ACTIVE,
            fg=TITLE_FG,
            anchor="center"
        )
        self.title_lbl.pack(side="left", expand=True, fill="x")

        if not self.flags & WindowFlags.WN_CONTROLS:
            self.min_btn = tk.Label(
                self.titlebar,
                text="▁",
                bg=TITLE_ACTIVE,
                fg=TITLE_FG,
                width=3
            )
            self.min_btn.pack(side="right")

            self.max_btn = tk.Label(
                self.titlebar,
                text="▢",
                bg=TITLE_ACTIVE,
                fg=TITLE_FG,
                width=3
            )
            self.max_btn.pack(side="right")

            self.min_btn.bind("<Button-1>", self.minimize)
            self.max_btn.bind("<Button-1>", self.maximize)

        self.menu_btn.bind("<Button-1>", self.show_menu)

    # ================= CONTENT =================

    def _create_content(self):
        self.content = tk.Frame(
            self.frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="black"
        )
        self.content.pack(fill="both", expand=True)

    # ================= EVENTS =================

    def _bind_window(self):

        for widget in [self.titlebar, self.title_lbl, self.menu_btn]:
            widget.bind("<ButtonPress-1>", self.start_drag)
            widget.bind("<B1-Motion>", self.drag)
            widget.bind("<ButtonRelease-1>", self.stop_drag)
        self.menu_btn.bind("<Button-1>", self.show_menu)
        if hasattr(self, "min_btn"):
            self.min_btn.bind("<Button-1>", self.minimize)
        if hasattr(self, "max_btn"):
            self.max_btn.bind("<Button-1>", self.maximize)

    def activate(self, event=None):
        if Window.active_window and Window.active_window != self:
            Window.active_window.deactivate()

        self.frame.lift()
        self.titlebar.config(bg=TITLE_ACTIVE)
        self.title_lbl.config(bg=TITLE_ACTIVE)
        self.menu_btn.config(bg=TITLE_ACTIVE)
        if hasattr(self, "min_btn"):
            self.min_btn.config(bg=TITLE_ACTIVE)
            self.max_btn.config(bg=TITLE_ACTIVE)

        Window.active_window = self

    def deactivate(self):
        self.titlebar.config(bg=TITLE_INACTIVE)
        self.title_lbl.config(bg=TITLE_INACTIVE)
        self.menu_btn.config(bg=TITLE_INACTIVE)
        if hasattr(self, "min_btn"):
            self.min_btn.config(bg=TITLE_INACTIVE)
            self.max_btn.config(bg=TITLE_INACTIVE)

    # ================= DRAG =================

    def start_drag(self, e):
        if self.flags & WindowFlags.WN_DRAGABLE == 0:
            return
        if e.widget == self.menu_btn:  # не перетаскиваем, если клик по меню
            return
        self.activate()
        self.is_dragging = True

        # координаты курсора относительно родителя
        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        self.dx = e.x_root - parent_x - self.frame.winfo_x()
        self.dy = e.y_root - parent_y - self.frame.winfo_y()
        # print(f"[DEBUG] start_drag: dx={self.dx}, dy={self.dy}")

    def drag(self, e):
        if not self.is_dragging or self.is_maximized:
            return

        # ограничиваем окно рамками родителя
        parent_w = self.parent.winfo_width()
        parent_h = self.parent.winfo_height()
        win_w = self.frame.winfo_width()
        win_h = self.frame.winfo_height()

        x = e.x_root - self.parent.winfo_rootx() - self.dx
        y = e.y_root - self.parent.winfo_rooty() - self.dy

        # ограничение координат
        x = max(0, min(x, parent_w - win_w))
        y = max(0, min(y, parent_h - win_h))

        self.frame.place(x=x, y=y)
        # print(f"[DEBUG] drag: x={x}, y={y}")

    def stop_drag(self, e):
        # print(f"[DEBUG] stop_drag called")
        self.is_dragging = False

    # ================= WINDOW OPS =================

    def maximize(self, e=None):
        if self.is_maximized:
            self.restore()
            return

        self.prev_geom = (
            self.frame.winfo_x(),
            self.frame.winfo_y(),
            self.frame.winfo_width(),
            self.frame.winfo_height()
        )

        pw = self.parent.winfo_width()
        ph = self.parent.winfo_height()
        self.frame.place(x=0, y=0, width=pw, height=ph)
        self.is_maximized = True

    def restore(self):
        if self.is_minimized:
            x, y, w, h = self.prev_geom
            self.frame.place(x=x, y=y, width=w, height=h)
            self.content.pack(fill="both", expand=True)  # показываем контент
            self.is_minimized = False
            return

        if self.is_maximized:
            x, y, w, h = self.prev_geom
            self.frame.place(x=x, y=y, width=w, height=h)
            self.is_maximized = False

    def minimize(self, e=None):
        if self.is_minimized:
            return

        # сохраняем полную геометрию
        self.prev_geom = (
            self.frame.winfo_x(),
            self.frame.winfo_y(),
            self.frame.winfo_width(),
            self.frame.winfo_height()
        )

        # сворачиваем контент, оставляя только titlebar
        self.content.pack_forget()  # скрываем контент
        frame_height = self.titlebar.winfo_height()
        self.frame.place(height=frame_height)  # уменьшаем высоту окна
        self.is_minimized = True

    def close(self):
        if self in getattr(self.parent, "childs", []):
            self.parent.childs.remove(self)
        if Window.active_window == self:
            Window.active_window = None
        self.frame.destroy()
        self.frame = None
        self.content = None
        self.titlebar = None

    def show_menu(self, e):
        menu = tk.Menu(self.frame, tearoff=0)
        menu.add_command(label="Restore", command=self.restore)
        menu.add_command(label="Minimize", command=self.minimize)
        menu.add_command(label="Maximize", command=self.maximize)
        menu.add_separator()
        menu.add_command(label="Close", command=self.close)
        menu.tk_popup(e.x_root, e.y_root)
        return "break"


    # ================= CONTENT =================

    def set_content(self, content_cls):
        for w in self.content.winfo_children():
            w.destroy()
        widget = content_cls(self.content)
        widget.pack(fill="both", expand=True)

    # ================= CHILD =================

    def create_child(self, title, content, size, flags=0):
        child = Window(self.content, title, content, size, flags)
        self.childs.append(child)
        return child
