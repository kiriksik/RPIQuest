import tkinter as tk

from widgets.login_window import LoginWindowContent
from widgets.window.flags import WindowFlags
from desktop.desktop import Desktop
from gpio_mock import GaletteMock
from styles import WIN_BG, WIN_DARK, WIN_LIGHT, WIN_BLACK, DESKTOP_BG, TITLE_BG_ACTIVE, TITLE_BG_INACTIVE, TITLE_FG, FONT_NORMAL, FONT_TITLE, FONT_BIG
from game_logic import GameState
from control_panel import ControlPanel
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, APP_TITLE,
    LEVEL_MAX, LEVEL_RISE_INTERVAL, ALARM_DELAY,
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
        # self.show_desktop()
    # ================== ЗАГРУЗКА ==================
    def show_boot_screen(self):
        self.clear_frame()
        from boot.bios_boot import BIOSBoot
        BIOSBoot(self.frame, on_complete=self.show_password_screen, width=SCREEN_WIDTH, height=SCREEN_HEIGHT)


    # ================== ПАРОЛЬ ==================
    def show_password_screen(self):
        self.clear_frame()

        outer = tk.Frame(
            self.frame,
            bg=WIN_BG,
            bd=2,
            relief="raised"
        )
        outer.place(relx=0.5, rely=0.5, anchor="center", width=320, height=200)

        inner = tk.Frame(
            outer,
            bg=WIN_BG,
            bd=2,
            relief="sunken"
        )
        inner.pack(fill="both", expand=True, padx=4, pady=4)

        users = [
            {"name": "Василий", "avatar": None},
            {"name": "Оператор", "avatar": None},
        ]

        LoginWindowContent(inner, self, users).pack(fill="both", expand=True)

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

        self.state.level_running = True
        self.schedule_level_rise()

    def schedule_level_rise(self):
        if not self.state.level_running:
            return

        if self.state.alarm_mode:
            self.state.increase_alarm_level()
        else:
            self.state.increase_levels()


        if self.state.alarm_triggered:
            self.show_alarm_screen()
            return

        self.root.after(LEVEL_RISE_INTERVAL, self.schedule_level_rise)


    # ================== АВАРИЙНЫЙ ЭКРАН ==================

    def show_error_dialog(self):
        error = tk.Toplevel(self.root)
        error.geometry("420x220")
        error.resizable(False, False)
        error.configure(bg="blue")
        error.grab_set()  # модальное окно
        error.transient(self.root)

        # ===== TITLE BAR =====
        title_bar = tk.Frame(error, bg="blue", height=28)
        title_bar.pack(fill="x")

        tk.Label(
            title_bar,
            text="ШТИЛЬ МОНИТОР 0.9b",
            fg="white",
            bg="blue",
            font=FONT_TITLE
        ).pack(side="left", padx=8)

        # ===== CONTENT =====
        content = tk.Frame(error, bg="white", bd=2, relief="sunken")
        content.pack(fill="both", expand=True, padx=4, pady=4)

        # ===== STOP SIGN =====
        canvas = tk.Canvas(content, width=80, height=80, bg="white", highlightthickness=0)
        canvas.place(x=20, y=40)

        # восьмиугольник STOP
        stop_points = [
            20, 0, 60, 0, 80, 20, 80, 60,
            60, 80, 20, 80, 0, 60, 0, 20
        ]
        canvas.create_polygon(stop_points, fill="red", outline="black")
        canvas.create_text(40, 40, text="STOP", fill="white", font=("Courier", 12, "bold"))

        # ===== TEXT =====
        tk.Label(
            content,
            text="Аварийное завершение\nпрограммы",
            bg="white",
            fg="black",
            font=FONT_BIG,
            justify="center"
        ).place(relx=0.6, rely=0.45, anchor="center")

        # ===== OK BUTTON =====
        ok_btn = tk.Frame(
            content,
            bg=WIN_LIGHT,
            bd=2,
            relief="raised"
        )
        ok_btn.place(relx=0.5, rely=0.82, anchor="center", width=80, height=28)

        ok_label = tk.Label(
            ok_btn,
            text="OK",
            bg=WIN_LIGHT,
            fg="black",
            font=FONT_NORMAL
        )
        ok_label.pack(expand=True)

        def close_all(event=None):
            error.destroy()
            self.show_desktop()

        ok_btn.bind("<Button-1>", close_all)
        ok_label.bind("<Button-1>", close_all)

        # ================== РАБОЧИЙ СТОЛ ==================
    def enter_desktop(self, error_window):
        error_window.destroy()
        self.show_desktop()

    def show_desktop(self):
        self.clear_frame()
        self.desktop = Desktop(self.frame, self)
        self.desktop.pack(fill="both", expand=True)

    def open_notepad(self):
        from apps.notepad import NotepadContent
        self.desktop.wm.create_window(
            title="Notepad",
            content=lambda p: NotepadContent(p, text=STORY_TEXT),
            size=(120, 100, 500, 350),
            flags=WindowFlags.WN_DRAGABLE
        )

    def open_calc(self):
        from apps.calculator import CalculatorContent
        self.desktop.wm.create_window(
            title="Calculator",
            content=CalculatorContent,
            size=(160, 120, 220, 260),
            flags=WindowFlags.WN_DRAGABLE
        )

    # ================== АВАРИЙНЫЙ ЭКРАН ==================
    def show_alarm_screen(self):


        # через паузу — системная ошибка
        self.root.after(2000, self.show_error_dialog)

    # ================== УТИЛИТЫ ==================
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

