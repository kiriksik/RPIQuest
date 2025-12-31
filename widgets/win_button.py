import tkinter as tk
from styles import WIN_BG, WIN_DARK, WIN_BLACK, FONT_NORMAL


class WinButton(tk.Frame):
    """
    Кнопка в стиле Windows 3.1
    """

    def __init__(
        self,
        parent,
        text,
        command=None,
        width=80,
        height=25,
        disabled=False
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=WIN_BG,
            highlightthickness=1,
            highlightbackground=WIN_BLACK,
            relief="raised",
            bd=2
        )

        self.pack_propagate(False)
        self.command = command
        self.disabled = disabled
        self.pressed = False

        # ===== LABEL =====
        self.label = tk.Label(
            self,
            text=text,
            bg=WIN_BG,
            fg=WIN_BLACK,
            font=FONT_NORMAL
        )
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        if not self.disabled:
            self._bind_events()
        else:
            self.label.config(fg=WIN_DARK)

    # ================= EVENTS =================

    def _bind_events(self):
        for widget in (self, self.label):
            widget.bind("<ButtonPress-1>", self._on_press)
            widget.bind("<ButtonRelease-1>", self._on_release)
            widget.bind("<Leave>", self._on_leave)

    def _on_press(self, event):
        if self.disabled:
            return
        self.pressed = True
        self.config(relief="sunken", bg=WIN_DARK)
        self.label.config(bg=WIN_DARK)

    def _on_release(self, event):
        if self.disabled or not self.pressed:
            return

        self.pressed = False
        self.config(relief="raised", bg=WIN_BG)
        self.label.config(bg=WIN_BG)

        # Проверка: курсор всё ещё над кнопкой
        if self.winfo_containing(event.x_root, event.y_root) in (self, self.label):
            if self.command:
                self.command()

    def _on_leave(self, event):
        if self.disabled:
            return
        self.pressed = False
        self.config(relief="raised", bg=WIN_BG)
        self.label.config(bg=WIN_BG)

    # ================= API =================

    def set_enabled(self, value: bool):
        self.disabled = not value
        if self.disabled:
            self.label.config(fg=WIN_DARK)
        else:
            self.label.config(fg=WIN_BLACK)
            self._bind_events()
