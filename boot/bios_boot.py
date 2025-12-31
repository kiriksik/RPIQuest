import tkinter as tk
import random


BIOS_HEADER = [
    "American Megatrends Inc.",
    "AMIBIOS (C)1992 American Megatrends Inc.",
    "BIOS Date: 09/18/94  Ver: 4.51PG",
    ""
]

POST_BLOCK = [
    "CPU : Intel(R) 80486DX-33",
    "FPU : Internal",
    "Clock : 33MHz",
    "Cache Memory : 8KB",
    "",
    "Checking NVRAM.....OK",
    "Checking CMOS.....OK",
    "",
    "Detecting IDE Drives ...",
    "Primary Master : ST31276A",
    "Primary Slave  : None",
    "Secondary Master : None",
    "Secondary Slave  : None",
    "",
    "Detecting Floppy Drives ...",
    "Drive A: 1.44MB 3.5\"",
    "Drive B: None",
    "",
    "Detecting Serial Ports ...",
    "COM1 : 3F8",
    "COM2 : 2F8",
    "",
    "Detecting Parallel Ports ...",
    "LPT1 : 378",
    "",
]

FINAL_LINES = [
    "",
    "Press <DEL> to enter SETUP",
    "",
    "Booting from C:\\"
]


class BIOSBoot(tk.Frame):
    def __init__(self, parent, on_complete, width, height):
        super().__init__(parent, bg="black")
        self.pack(fill="both", expand=True)

        self.on_complete = on_complete

        self.canvas = tk.Canvas(
            self,
            bg="black",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.x = 10
        self.y = 10
        self.line_height = 18
        self.cursor_visible = True

        self.text_items = []
        self.after(200, self.start_boot)

    # ================= START =================

    def start_boot(self):
        for line in BIOS_HEADER:
            self._print(line)
        self.after(500, self.memory_test)

    # ================= MEMORY TEST =================

    def memory_test(self):
        self.mem_value = 0
        self.mem_max = 65536
        self.mem_text = self.canvas.create_text(
            self.x, self.y,
            anchor="nw",
            fill="#C0C0C0",
            font=("Courier New", 11),
            text="Memory Test : 00000 KB"
        )
        self.y += self.line_height
        self.after(30, self._memory_step)

    def _memory_step(self):
        if self.mem_value < self.mem_max:
            self.mem_value += random.randint(512, 2048)
            if self.mem_value > self.mem_max:
                self.mem_value = self.mem_max
            self.canvas.itemconfig(
                self.mem_text,
                text=f"Memory Test : {self.mem_value:05d} KB"
            )
            self.after(20, self._memory_step)
        else:
            self.canvas.itemconfig(
                self.mem_text,
                text=f"Memory Test : {self.mem_max:05d} KB OK"
            )
            self.after(400, self.post_sequence)

    # ================= POST =================

    def post_sequence(self):
        self.post_index = 0
        self.after(200, self._post_step)

    def _post_step(self):
        if self.post_index < len(POST_BLOCK):
            self._print(POST_BLOCK[self.post_index])
            self.post_index += 1
            self.after(120, self._post_step)
        else:
            self.after(400, self.final_stage)

    # ================= FINAL =================

    def final_stage(self):
        for line in FINAL_LINES:
            self._print(line)
        self.after(800, self.finish)

    # ================= UTIL =================

    def _print(self, text):
        self.canvas.create_text(
            self.x, self.y,
            anchor="nw",
            fill="#C0C0C0",
            font=("Courier New", 11),
            text=text
        )
        self.y += self.line_height

    def finish(self):
        self.destroy()
        self.on_complete()
