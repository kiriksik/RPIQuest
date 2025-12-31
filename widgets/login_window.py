import tkinter as tk
from tkinter import ttk
from styles import WIN_BG, WIN_BLACK, FONT_NORMAL
from widgets.win_button import WinButton


class LoginWindowContent(tk.Frame):
    """
    Экран входа в стиле Windows 3.1
    """

    def __init__(self, parent, app, users):
        super().__init__(parent, bg=WIN_BG)

        self.app = app
        self.users = users

        self.selected_user = tk.StringVar()
        self.password_var = tk.StringVar()

        self._create_ui()

    def _create_ui(self):
        frame = tk.Frame(self, bg=WIN_BG)
        frame.pack(expand=True, fill="both", padx=12, pady=12)

        # ===== USER =====
        tk.Label(
            frame,
            text="Select User:",
            bg=WIN_BG,
            fg=WIN_BLACK,
            font=FONT_NORMAL
        ).pack(anchor="w")

        names = [u["name"] for u in self.users]
        self.user_combo = ttk.Combobox(
            frame,
            values=names,
            textvariable=self.selected_user,
            state="readonly",
            width=25
        )
        self.user_combo.pack(pady=6)
        self.user_combo.bind("<<ComboboxSelected>>", lambda e: self._focus_password())



        # ===== PASSWORD =====
        tk.Label(
            frame,
            text="Password:",
            bg=WIN_BG,
            fg=WIN_BLACK,
            font=FONT_NORMAL
        ).pack(anchor="w", pady=(10, 0))

        self.pass_entry = tk.Entry(
            frame,
            textvariable=self.password_var,
            show="*",
            font=FONT_NORMAL,
            width=25
        )
        self.pass_entry.pack(pady=4)
        self.pass_entry.bind("<Return>", self._submit)

        self._create_numpad(frame)

        # ===== ERROR =====
        self.error_label = tk.Label(
            frame,
            text="",
            fg="red",
            bg=WIN_BG,
            font=FONT_NORMAL
        )
        self.error_label.pack(pady=4)

        # ===== BUTTONS =====
        btns = tk.Frame(frame, bg=WIN_BG)
        btns.pack(pady=10)

        WinButton(btns, "OK", command=self._submit, width=70).pack(side="left", padx=6)
        WinButton(btns, "Cancel", command=self._cancel, width=70).pack(side="left", padx=6)

    def _create_numpad(self, parent):
        pad = tk.Frame(parent, bg=WIN_BG)
        pad.pack(pady=8)

        buttons = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("←", 3, 0), ("0", 3, 1), ("C", 3, 2),
        ]

        for text, r, c in buttons:
            WinButton(
                pad,
                text,
                width=45,
                command=lambda t=text: self._numpad_press(t)
            ).grid(row=r, column=c, padx=4, pady=4)

    def _numpad_press(self, key):
        if key.isdigit():
            self.password_var.set(self.password_var.get() + key)

        elif key == "←":
            self.password_var.set(self.password_var.get()[:-1])

        elif key == "C":
            self.password_var.set("")

        self.pass_entry.focus()

    def _focus_password(self):
        self.pass_entry.focus()
        self.error_label.config(text="")

    def _submit(self, event=None):
        user = self.selected_user.get()
        password = self.password_var.get()

        if user == "Оператор" and password == "4848":
            print("[ADMIN] EXIT TO OS")
            self.app.gpio.cleanup()
            self.app.server.close()
            self.app.root.quit()
            return
        if user == "Василий" and password == "2018":
            self.app.server.send("passwordOk")
            self.app.show_control_panel()

            self.app.show_control_panel()
        else:

            self.error_label.config(text="ACCESS DENIED")
            self.password_var.set("")
            self.pass_entry.focus()

    def _cancel(self):
        self.password_var.set("")
        self.error_label.config(text="")
