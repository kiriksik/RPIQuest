import tkinter as tk
from gpio_mock import GaletteMock
from styles import WIN_BG, WIN_DARK, WIN_LIGHT, WIN_BLACK, DESKTOP_BG, TITLE_BG_ACTIVE, TITLE_BG_INACTIVE, TITLE_FG, FONT_NORMAL, FONT_TITLE, FONT_BIG
from widgets import WinButton, WinWindow
from game_logic import GameState
from control_panel import ControlPanel
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, APP_TITLE,
    LEVEL_MAX, LEVEL_RISE_INTERVAL, ALARM_DELAY,
    RECOMMENDED_POSITIONS, FAST_RISE_INTERVAL,
    STORY_TEXT, STEP_AMOUNT, STEP_DELAY
)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=WIN_BG)

        self.state = GameState()
        self.galette = GaletteMock()

        # ====== ОСНОВНОЙ ФРЕЙМ ======
        self.frame = tk.Frame(self.root, bg=WIN_BG)
        self.frame.pack(fill="both", expand=True)

        # запуск экрана загрузки
        self.root.after(100, self.show_boot_screen)

    # ================== ЗАГРУЗКА ==================
    def show_boot_screen(self):
        self.clear_frame()
        self.boot_label = tk.Label(
            self.frame,
            text="Microsoft Windows 3.1",
            fg=WIN_LIGHT,
            bg=WIN_BG,
            font=FONT_BIG
        )
        self.boot_label.pack(pady=50)

        # Прогресс-бар с 3D рамкой
        self.progress_canvas = tk.Canvas(
            self.frame,
            width=400,
            height=30,
            bg=WIN_BG,
            highlightthickness=2,
            highlightbackground=WIN_BLACK,
            relief="sunken"
        )
        self.progress_canvas.pack(pady=20)

        self.progress_rect = self.progress_canvas.create_rectangle(0, 0, 0, 30, fill=WIN_LIGHT)
        self.boot_progress = 0
        self.blink_boot_label()
        self.boot_step()

    def boot_step(self):
        if not hasattr(self, "progress_canvas") or not self.progress_canvas.winfo_exists():
            return
        if self.boot_progress >= 100:
            self.show_password_screen()
            return
        self.boot_progress += STEP_AMOUNT
        width = int(400 * self.boot_progress / 100)
        self.progress_canvas.coords(self.progress_rect, 0, 0, width, 30)
        self.root.after(STEP_DELAY, self.boot_step)

    def blink_boot_label(self):
        if not hasattr(self, "boot_label") or not self.boot_label.winfo_exists():
            return
        color = WIN_LIGHT if self.boot_label.cget("fg") == WIN_DARK else WIN_DARK
        self.boot_label.config(fg=color)
        self.root.after(200, self.blink_boot_label)

    # ================== ПАРОЛЬ ==================
    def show_password_screen(self):
        self.clear_frame()
        label_frame = tk.Frame(self.frame, bg=WIN_BG, bd=2, relief="sunken")
        label_frame.pack(pady=50)
        self.label = tk.Label(label_frame, text="ENTER PASSWORD", fg=WIN_BLACK, bg=WIN_BG, font=FONT_BIG)
        self.label.pack(padx=10, pady=5)

        entry_frame = tk.Frame(self.frame, bg=WIN_BG, bd=2, relief="sunken")
        entry_frame.pack()
        self.entry = tk.Entry(entry_frame, show="*", font=FONT_NORMAL, justify="center", bd=0)
        self.entry.pack(padx=4, pady=4)
        self.entry.focus()

        self.error_label = tk.Label(self.frame, text="", fg="red", bg=WIN_BG, font=FONT_NORMAL)
        self.error_label.pack(pady=10)
        self.entry.bind("<Return>", self.check_password)

    def check_password(self, event=None):
        password = self.entry.get()
        if self.state.check_password(password):
            self.show_control_panel()
        else:
            self.error_label.config(text="ACCESS DENIED")
            self.entry.delete(0, tk.END)

    # ================== ПАНЕЛЬ УПРАВЛЕНИЯ ==================
    def show_control_panel(self):
        self.clear_frame()
        self.panel = ControlPanel(
            self.frame,
            self.state,
            on_alarm=self.show_alarm_screen
        )
        self.panel.pack(fill="both", expand=True)

    def schedule_level_rise(self):
        if not self.state.level_running:
            return

        if self.state.alarm_mode:
            self.state.increase_alarm_level()
        else:
            self.state.increase_levels()

        self.update_water()

        if self.state.alarm_triggered:
            self.show_alarm_screen()
            return

        self.root.after(LEVEL_RISE_INTERVAL, self.schedule_level_rise)


    # ================== АВАРИЙНЫЙ ЭКРАН ==================

    def show_error_dialog(self):
        error = tk.Toplevel(self.root)
        error.title("System Error")
        error.geometry("300x150")
        error.configure(bg=WIN_BG)
        label = tk.Label(error, text="FATAL ERROR\nSYSTEM HALTED", bg=WIN_BG, fg="black", font=FONT_NORMAL)
        label.pack(pady=20)
        btn = WinButton(error, "OK", command=lambda: self.enter_desktop(error), width=80, height=25)
        btn.pack()

    # ================== РАБОЧИЙ СТОЛ ==================
    def enter_desktop(self, error_window):
        error_window.destroy()
        self.show_desktop()

    def show_desktop(self):
        self.clear_frame()
        self.desktop = tk.Frame(self.frame, bg=DESKTOP_BG)
        self.desktop.pack(fill="both", expand=True)
        win = WinWindow(self.desktop, "Program Manager", 260, 180)
        win.place(x=40, y=40)
        WinButton(win.content, "Notepad", command=self.open_notepad, width=100).pack(pady=10)
        WinButton(win.content, "Calculator", command=self.open_calc, width=100).pack()

    def open_notepad(self):
        win = tk.Toplevel(self.root)
        win.title("Notepad")
        win.geometry("600x400")
        win.configure(bg=WIN_BG)
        text = tk.Text(win, font=FONT_NORMAL, bg=WIN_LIGHT, fg=WIN_BLACK, relief="sunken", borderwidth=2)
        text.pack(fill="both", expand=True, padx=4, pady=4)
        text.insert("1.0", STORY_TEXT)
        text.config(state="disabled")

    def open_calc(self):
        win = tk.Toplevel(self.root)
        win.title("Calculator")
        win.geometry("220x260")
        win.configure(bg=WIN_BG)
        label = tk.Label(win, text="Calculator\n(not implemented)", bg=WIN_BG, fg=WIN_BLACK, font=FONT_NORMAL)
        label.pack(expand=True)

    # ================== АВАРИЙНЫЙ ЭКРАН ==================
    def show_alarm_screen(self):
        self.state.level_running = False
        self.clear_frame()

        self.alarm_label = tk.Label(
            self.frame,
            text="АВАРИЙНАЯ ОСТАНОВКА",
            fg="red",
            bg=WIN_BG,
            font=FONT_BIG
        )
        self.alarm_label.pack(pady=40)

        self.sub_label = tk.Label(
            self.frame,
            text="КРИТИЧЕСКИЙ УРОВЕНЬ ВОДЫ",
            fg="red",
            bg=WIN_BG,
            font=FONT_NORMAL
        )
        self.sub_label.pack()

        # через паузу — системная ошибка
        self.root.after(2000, self.show_error_dialog)

    # ================== УТИЛИТЫ ==================
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

