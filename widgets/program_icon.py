import tkinter as tk
from PIL import Image, ImageTk
from styles import WIN_BG, WIN_BLACK, FONT_NORMAL

ICON_SIZE = (40, 40)  # фиксированный размер иконки

class ProgramIcon(tk.Frame):
    def __init__(self, parent, text, command=None, image_path=None):
        super().__init__(
            parent,
            bg=WIN_BG,
            width=80,
            height=80,
            highlightbackground=WIN_BLACK,
            highlightthickness=1
        )
        self.command = command
        self.pack_propagate(False)

        # 🔹 иконка
        if image_path:
            pil_img = Image.open(image_path)
            pil_img = pil_img.resize(ICON_SIZE, Image.Resampling.LANCZOS)  # ресайз
            self.img = ImageTk.PhotoImage(pil_img)
            icon_label = tk.Label(self, image=self.img, bg=WIN_BG)
            icon_label.pack(pady=4)
        else:
            icon = tk.Canvas(self, width=ICON_SIZE[0], height=ICON_SIZE[1], bg=WIN_BG, highlightthickness=0)
            icon.create_rectangle(0, 0, ICON_SIZE[0]-1, ICON_SIZE[1]-1, fill="white", outline="black")
            icon.pack(pady=4)

        # 🔹 текст под иконкой
        label = tk.Label(
            self,
            text=text,
            bg=WIN_BG,
            fg="black",
            font=FONT_NORMAL,
            wraplength=80,
            justify="center"
        )
        label.pack()

        # 🔹 клик по любой части
        for w in (self, label):
            w.bind("<Button-1>", self._click)
        if image_path:
            icon_label.bind("<Button-1>", self._click)
        else:
            icon.bind("<Button-1>", self._click)

    def _click(self, event=None):
        if self.command:
            self.command()
