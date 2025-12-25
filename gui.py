import tkinter as tk
from gpio_mock import GaletteMock

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    APP_TITLE,
    LEVEL_MAX,
    LEVEL_RISE_INTERVAL,
    ALARM_DELAY,
    RECOMMENDED_POSITIONS,
    FAST_RISE_INTERVAL
)
from game_logic import GameState


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg="black")

        self.state = GameState()
        self.galette = GaletteMock()

        # ====== ОСНОВНОЙ ФРЕЙМ ======
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(expand=True)

        self.show_black_screen()

        # временно — эмуляция команды startPC
        self.root.after(1000, self.start_pc)

    # ====== ЭКРАН 1: ЧЁРНЫЙ ЭКРАН ======
    def show_black_screen(self):
        self.clear_frame()

        self.label = tk.Label(
            self.frame,
            text="BLACK SCREEN",
            fg="green",
            bg="black",
            font=("Courier", 18)
        )
        self.label.pack(pady=20)

        self.sub_label = tk.Label(
            self.frame,
            text="waiting for startPC...",
            fg="green",
            bg="black",
            font=("Courier", 12)
        )
        self.sub_label.pack()

    # ====== СТАРТ ПК ======
    def start_pc(self):
        self.state.start_pc()
        self.show_password_screen()

    # ====== ЭКРАН 2: ВВОД ПАРОЛЯ ======
    def show_password_screen(self):
        self.clear_frame()

        self.label = tk.Label(
            self.frame,
            text="ENTER PASSWORD",
            fg="green",
            bg="black",
            font=("Courier", 18)
        )
        self.label.pack(pady=20)

        self.entry = tk.Entry(
            self.frame,
            show="*",
            font=("Courier", 16),
            justify="center"
        )
        self.entry.pack()
        self.entry.focus()

        self.error_label = tk.Label(
            self.frame,
            text="",
            fg="red",
            bg="black",
            font=("Courier", 12)
        )
        self.error_label.pack(pady=10)

        self.entry.bind("<Return>", self.check_password)

    def check_password(self, event=None):
        password = self.entry.get()

        if self.state.check_password(password):
            self.show_control_panel()
            self.update_water()
            self.schedule_level_rise()
        else:
            self.error_label.config(text="ACCESS DENIED")
            self.entry.delete(0, tk.END)

    # ====== ЭКРАН 3: ПАНЕЛЬ УПРАВЛЕНИЯ ======
    def show_control_panel(self):
        self.clear_frame()

        self.title_label = tk.Label(
            self.frame,
            text="CONTROL PANEL\nSHUTTER #1",
            fg="green",
            bg="black",
            font=("Courier", 16)
        )
        self.title_label.pack(pady=10)

        self.canvas = tk.Canvas(
            self.frame,
            width=300,
            height=400,
            bg="black",
            highlightthickness=1,
            highlightbackground="green"
        )
        self.canvas.pack(pady=20)
        self.pos_label = tk.Label(
            self.frame,
            text="Position: 1",
            fg="green",
            bg="black",
            font=("Courier", 12)
        )
        self.pos_label.pack(pady=5)

        self.stage_label = tk.Label(
            self.frame,
            text=f"Required: {RECOMMENDED_POSITIONS[self.state.stage_index]}",
            fg="yellow",
            bg="black",
            font=("Courier", 12)
        )
        self.stage_label.pack(pady=5)

        self.status_label = tk.Label(
            self.frame,
            text="Status: READY",
            fg="green",
            bg="black",
            font=("Courier", 12)
        )

        # ====== КНОПКИ ГАЛЕТНИКА (ТЕСТ) ======
        buttons_frame = tk.Frame(self.frame, bg="black")
        buttons_frame.pack(pady=10)

        for i in range(1, 12):
            btn = tk.Button(
                buttons_frame,
                text=str(i),
                width=3,
                command=lambda p=i: self.on_galette_change(p)
            )
            btn.grid(row=(i - 1) // 6, column=(i - 1) % 6, padx=2, pady=2)

        self.water_rect = self.canvas.create_rectangle(
            50, 400, 250, 400,
            fill="blue"
        )

    # ====== ВОДА ======
    def update_water(self):
        level_ratio = self.state.level / LEVEL_MAX
        height = int(400 * level_ratio)

        self.canvas.coords(
            self.water_rect,
            50,
            400 - height,
            250,
            400
        )

    def schedule_level_rise(self):
        if not self.state.level_running:
            return

        if self.state.alarm_mode:
            self.state.increase_alarm_level()
            self.update_water()

            if self.state.alarm_triggered:
                self.show_alarm_screen()
                return

            self.root.after(FAST_RISE_INTERVAL, self.schedule_level_rise)
        else:
            self.state.increase_level()
            self.update_water()
            self.root.after(LEVEL_RISE_INTERVAL, self.schedule_level_rise)

    # ====== УТИЛИТЫ ======
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

    def on_galette_change(self, pos: int):
        self.galette.set_position(pos)

        before_stage = self.state.stage_index
        before_level = self.state.level

        self.state.set_galette_position(pos)

        self.pos_label.config(text=f"Position: {pos}")

        if self.state.stage_index > before_stage:
            self.status_label.config(text="Status: POSITION ACCEPTED", fg="green")
            self.update_water()

        else:
            if self.state.level < LEVEL_MAX:
                self.status_label.config(text="Status: LEVEL TOO LOW", fg="orange")
            else:
                self.status_label.config(text="Status: WRONG POSITION", fg="red")

        if self.state.stage_index < len(RECOMMENDED_POSITIONS):
            required = RECOMMENDED_POSITIONS[self.state.stage_index]
            self.stage_label.config(text=f"Required: {required}")
        else:
            self.stage_label.config(text="Sequence complete")
            self.status_label.config(text="Status: COMPLETE", fg="cyan")

    def show_alarm_screen(self):
        self.clear_frame()

        self.alarm_label = tk.Label(
            self.frame,
            text="EMERGENCY STOP",
            fg="red",
            bg="black",
            font=("Courier", 20, "bold")
        )
        self.alarm_label.pack(pady=40)

        self.sub_label = tk.Label(
            self.frame,
            text="CRITICAL WATER LEVEL",
            fg="red",
            bg="black",
            font=("Courier", 14)
        )
        self.sub_label.pack()

        self.root.after(ALARM_DELAY, self.show_error_dialog)

    def show_error_dialog(self):
        error = tk.Toplevel(self.root)
        error.title("System Error")
        error.geometry("300x150")
        error.configure(bg="gray")

        label = tk.Label(
            error,
            text="FATAL ERROR\nSYSTEM HALTED",
            bg="gray",
            fg="black",
            font=("Courier", 10)
        )
        label.pack(pady=20)

        btn = tk.Button(
            error,
            text="OK",
            command=lambda: self.enter_desktop(error)
        )
        btn.pack()

    def enter_desktop(self, error_window):
        error_window.destroy()
        self.show_desktop()

    def show_desktop(self):
        self.clear_frame()

        self.desktop = tk.Frame(self.frame, bg="#008080")
        self.desktop.pack(fill="both", expand=True)

        note_btn = tk.Button(
            self.desktop,
            text="Notepad",
            width=12,
            command=self.open_notepad
        )
        note_btn.place(x=50, y=50)

    def open_notepad(self):
        win = tk.Toplevel(self.root)
        win.title("Notepad")
        win.geometry("600x400")

        text = tk.Text(win, font=("Courier", 10))
        text.pack(fill="both", expand=True)

        story = (
            "Привет.\n\n"
            "Проектор, который мы нашли, показывает что-то непонятное:\n"
            "вроде план нашего пункта управления, но какой-то другой.\n\n"
            "Наше здание было построено 94 года назад,\n"
            "после последнего крупного наводнения.\n\n"
            "Возможно, раньше было именно так."
        )

        text.insert("1.0", story)
        text.config(state="disabled")
