import tkinter as tk


from hardware.gpio_controller import GPIOController
from control_panel.control_panel import ControlPanel
from control_panel.alarm import AlarmWindow
from widgets.login_window import LoginWindowContent
from widgets.window.flags import WindowFlags
from desktop.desktop import Desktop
from gpio_mock import GaletteMock
from styles import WIN_BG, WIN_LIGHT, FONT_NORMAL, FONT_TITLE, FONT_BIG
from game_logic import GameState
from network.client import ServerClient
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, APP_TITLE,
    LEVEL_RISE_INTERVAL, ALARM_DELAY,
    STORY_TEXT, STEP_AMOUNT
)


class App:
    def __init__(self):
        self.server = ServerClient(server_host="192.168.0.201", port=80)
        self.gpio = GPIOController(
            galette_pins=[5, 6, 13, 19, 26, 12, 16, 20, 21, 25, 24],
            projector_input_pin=18,
            projector_relay_pin=23,

            on_galette_change=self.on_galette_change,
            on_projector_on=lambda: self.server.send("projectorOn"),
            on_projector_off=lambda: self.server.send("projectorOff"),
        )
        self.server.on_command = self._on_server_command_threadsafe

        self.server.start()
        self.root = tk.Tk()
        self.level_max_sent = False
        self.root.title(APP_TITLE)
        self.root.geometry(f"{SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        self.root.configure(bg=WIN_BG)

        self.state = GameState()
        self.galette = GaletteMock()

        # ====== ОСНОВНОЙ ФРЕЙМ ======
        self.frame = tk.Frame(self.root, bg=WIN_BG)
        self.frame.pack(fill="both", expand=True)

        # запуск экрана загрузки
        # self.root.after(100, self.show_boot_screen)
        # self.poll_galette()
        self.show_black_screen()
        # self.show_desktop()
    # ================== ЗАГРУЗКА ==================
    def _on_server_command_threadsafe(self, cmd: str):
        self.root.after(0, lambda: self.handle_server_command(cmd))

    def handle_server_command(self, cmd: str):
        print(f"[APP] CMD FROM SERVER: {cmd}")

        if cmd == "startPC":
            self.show_boot_screen()

        elif cmd == "reset":
            self.state.reset()
            self.show_black_screen()

        elif cmd == "exit":
            print("[APP] EXIT")
            self.gpio.cleanup()
            self.server.close()
            self.root.quit()

        elif cmd == "passPC":
            self.show_desktop()

        elif cmd == "passProjector":
            self.gpio.turn_relay_on()
            self.server.send("projectorOn")

        else:
            print(f"[APP] UNKNOWN CMD: {cmd}")

    def show_black_screen(self):
        self.clear_frame()
        black = tk.Frame(self.frame, bg="black")
        black.pack(fill="both", expand=True)

    def show_boot_screen(self):
        self.clear_frame()

        def after_bios():
            self.show_windows_splash()

        from boot.bios_boot import BIOSBoot
        BIOSBoot(
            self.frame,
            on_complete=after_bios,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT
        )

    def show_windows_splash(self):
        self.clear_frame()

        from boot.windows_splash import WindowsSplash

        WindowsSplash(
            self.frame,
            on_complete=self.show_password_screen,
            width=SCREEN_WIDTH,
            height=SCREEN_HEIGHT,
            duration=2500  # мс
        )

    def poll_galette(self):
        pos = self.galette.get_position()
        if pos:
            self.on_galette_change(pos)

        self.root.after(100, self.poll_galette)




    # ================== ПАРОЛЬ ==================
    def show_password_screen(self):
        self.clear_frame()

        outer = tk.Frame(
            self.frame,
            bg=WIN_BG,
            bd=2,
            relief="raised"
        )
        outer.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=360,
            height=420
        )

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
            app=self,
            on_alarm=self.show_alarm_screen,
            on_exit=self.show_desktop
        )
        self.panel.pack(fill="both", expand=True)

        self.state.level_running = True
        self.schedule_level_rise()

    def show_alarm_screen(self):
        self.state.level_running = False
        if hasattr(self, "panel"):
            self.panel.show_alarm_frame()

    def on_galette_change(self, pos):
        result = self.state.set_galette_position(pos)

        if result["result"] == "blocked":
            return

        self.send_events(result["events"])

        if result["result"] == "correct":
            self.state.start_movement()
            self.state.level_running = False

        elif result["result"] == "final":
            self.state.start_fast_alarm_rise()

    def send_events(self, events):
        for e in events:
            self.server.send(e)

    def schedule_level_rise(self):
        if not self.state.level_running:
            return

        if not self.state.alarm_mode:
            events = self.state.increase_levels(STEP_AMOUNT)
            self.send_events(events)
        else:
            events = self.state.increase_alarm_level()
            self.send_events(events)

        if self.state.alarm_triggered:
            self.root.after(ALARM_DELAY, self.show_error_dialog)
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
    def show_alarm_frame(self):
        if hasattr(self, "alarm_window"):
            return  # Уже показано

        def on_close_alarm():
            self.controls_locked = False
            del self.alarm_window

        self.controls_locked = True
        self.alarm_window = AlarmWindow(self, text="КРИТИЧЕСКИЙ УРОВЕНЬ ВОДЫ", on_close=on_close_alarm)
        self.alarm_window.place(x=100, y=100, width=300, height=150)

    # ================== УТИЛИТЫ ==================
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()






