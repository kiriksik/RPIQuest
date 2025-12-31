import tkinter as tk

class WindowsSplash(tk.Frame):
    def __init__(self, parent, on_complete, width, height, duration=2500):
        super().__init__(parent, bg="black")
        self.pack(fill="both", expand=True)

        self.on_complete = on_complete

        canvas = tk.Canvas(
            self,
            bg="black",
            highlightthickness=0
        )
        canvas.pack(fill="both", expand=True)

        # Центр
        cx = width // 2
        cy = height // 2

        # === ЛОГОТИП WINDOWS 3.1 (текстовый стиль) ===
        canvas.create_text(
            cx, cy - 30,
            text="Microsoft",
            fill="#C0C0C0",
            font=("Times New Roman", 20)
        )

        canvas.create_text(
            cx, cy + 5,
            text="WINDOWS",
            fill="#FFFFFF",
            font=("Arial Black", 36)
        )

        canvas.create_text(
            cx, cy + 45,
            text="Version 3.1",
            fill="#C0C0C0",
            font=("Courier New", 14)
        )

        canvas.create_text(
            cx, height - 40,
            text="Starting Windows...",
            fill="#808080",
            font=("Courier New", 11)
        )

        # Таймер
        self.after(duration, self.finish)

    def finish(self):
        self.destroy()
        self.on_complete()
