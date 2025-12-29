import tkinter as tk

class AlarmWindow(tk.Frame):
    def __init__(self, parent, text="АВАРИЙНАЯ ОСТАНОВКА", on_close=None):
        super().__init__(parent, bg="red", bd=2, relief="raised")
        self.on_close = on_close

        # ===== TITLE BAR =====
        self.title_bar = tk.Frame(self, bg="darkred", height=22)
        self.title_bar.pack(fill="x")

        tk.Label(
            self.title_bar,
            text="ALARM",
            bg="darkred",
            fg="white",
            font=("Arial", 9, "bold")
        ).pack(side="left", padx=6)

        close_btn = tk.Label(
            self.title_bar,
            text="X",
            bg="darkred",
            fg="white",
            font=("Arial", 9, "bold")
        )
        close_btn.pack(side="right", padx=6)
        close_btn.bind("<Button-1>", self.close)

        # ===== CONTENT =====
        self.content = tk.Frame(self, bg="white")
        self.content.pack(fill="both", expand=True)

        self.label = tk.Label(
            self.content,
            text=text,
            fg="red",
            bg="white",
            font=("Arial", 13, "bold"),
            wraplength=260,
            justify="center",
            anchor="center"
        )
        self.label.pack(expand=True, padx=10, pady=10)

    def close(self, event=None):
        if self.on_close:
            self.on_close()
        self.destroy()
