import tkinter as tk
from styles import WIN_BG, FONT_BIG
from widgets.win_button import WinButton


class CalculatorContent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=WIN_BG)
        self.current = ""
        self.operator = None
        self.acc = 0

        self.display = tk.Entry(self, justify="right", font=FONT_BIG, relief="sunken", bd=2)
        self.display.pack(fill="x", padx=6, pady=6)
        self.display.insert(0, "0")

        self._create_buttons()

    def add(self, value):
        if self.display.get() == "0":
            self.display.delete(0, tk.END)
        self.display.insert(tk.END, value)

    def op(self, operator):
        self.current = self.display.get()
        self.operator = operator
        self.display.delete(0, tk.END)

    def eq(self, _=None):
        try:
            if self.operator:
                expr = f"{self.current}{self.operator}{self.display.get()}"
                result = str(eval(expr))
                self.display.delete(0, tk.END)
                self.display.insert(0, result)
                self.current = ""
                self.operator = None
        except Exception:
            self.display.delete(0, tk.END)
            self.display.insert(0, "ERR")

    def clear(self, _=None):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.current = ""
        self.operator = None

    def _create_buttons(self):
        buttons = [
            ("7", self.add), ("8", self.add), ("9", self.add), ("/", self.op),
            ("4", self.add), ("5", self.add), ("6", self.add), ("*", self.op),
            ("1", self.add), ("2", self.add), ("3", self.add), ("-", self.op),
            ("0", self.add), ("C", self.clear), ("=", self.eq), ("+", self.op),
        ]

        grid = tk.Frame(self, bg=WIN_BG)
        grid.pack(padx=4, pady=4)

        for i, (txt, cmd) in enumerate(buttons):
            WinButton(
                grid,
                txt,
                command=lambda t=txt, c=cmd: c(t),
                width=45,
                height=30
            ).grid(row=i // 4, column=i % 4, padx=2, pady=2)
