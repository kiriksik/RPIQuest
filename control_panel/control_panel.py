import tkinter as tk
from styles import WIN_BG, WIN_DARK, WIN_LIGHT, WIN_BLACK, DESKTOP_BG, TITLE_BG_ACTIVE, TITLE_FG, FONT_NORMAL, FONT_TITLE, FONT_BIG
from game_logic import GameState
from config import LEVEL_MAX, RECOMMENDED_POSITIONS, LEVEL_RISE_INTERVAL, ALARM_DELAY, FAST_RISE_INTERVAL, SCREEN_HEIGHT, SCREEN_WIDTH, STEP_AMOUNT, FINAL_POSITION
import math

class ControlPanel(tk.Frame):
    def __init__(self, parent, state, app, on_alarm=None, on_exit=None):

        super().__init__(parent, bg="#A0C0E0", bd=2, relief="sunken")
        self.app = app
        self.state = state
        self.on_alarm = on_alarm
        self.on_exit = on_exit
        self.alarm_fired = False
        self.controls_locked = False
        self.alive = True
        self.alarm_visible = False

        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT

        self.configure(width=self.width, height=self.height)
        self.pack_propagate(False)
        self.pack()

        # ====== ПРОПОРЦИИ ======
        self.TOP_OFFSET = int(self.height * 0.05)
        self.TITLE_BAR_H = int(self.height * 0.05)
        self.TOP_MARGIN = int(self.height * 0.12)
        self.BOTTOM_MARGIN = int(self.height * 0.20)

        self.LEFT_COL_W = int(self.width * 0.25)
        self.RIGHT_COL_W = int(self.width * 0.60)

        self.CENTER_X = self.width // 2

        self.create_title_bar()
        self.create_panel_background()
        self.create_titles()
        self.create_water_indicator()
        self.create_galette()
        self.create_bottom_labels()

        self.schedule_update()

    # ===== TITLE BAR =====
    def create_title_bar(self):
        self.title_bar = tk.Frame(self, bg="blue", height=self.TITLE_BAR_H)
        self.title_bar.place(x=0, y=0, width=self.width)

        tk.Label(
            self.title_bar,
            text="ШТИЛЬ МОНИТОР 0.9b",
            fg="white",
            bg="blue",
            font=FONT_TITLE
        ).pack(side="left", padx=8)

    # ===== BACKGROUND =====
    def create_panel_background(self):
        self.panel_bg = tk.Frame(self, bg="#A0C0E0")
        self.panel_bg.place(
            x=0,
            y=self.TITLE_BAR_H,
            width=self.width,
            height=self.height - self.TITLE_BAR_H
        )

    # ===== TITLES =====
    def create_titles(self):
        tk.Label(
            self,
            text="Панель управления затвором №1",
            font=(FONT_TITLE[0], FONT_TITLE[1], "bold"),
            bg="#A0C0E0",
            fg=WIN_BLACK
        ).place(x=self.CENTER_X, y=self.TITLE_BAR_H + 5, anchor="n")

        tk.Label(
            self,
            text="Управление затвором",
            font=FONT_NORMAL,
            bg="#A0C0E0",
            fg=WIN_BLACK
        ).place(x=self.CENTER_X, y=self.TOP_MARGIN - 10, anchor="n")

    # ===== WATER INDICATOR =====
    def create_water_indicator(self):
        canvas_h = int(self.height * 0.55)
        canvas_w = int(self.LEFT_COL_W * 0.6)

        self.canvas_h = canvas_h
        self.canvas_w = canvas_w

        self.water_x1 = int(canvas_w * 0.42)
        self.water_x2 = int(canvas_w * 0.75)

        self.scale_top = int(canvas_h * 0.05)
        self.scale_bottom = int(canvas_h * 0.95)

        self.canvas = tk.Canvas(
            self,
            width=canvas_w,
            height=canvas_h,
            bg=WIN_LIGHT,
            highlightthickness=2,
            highlightbackground="blue"
        )
        self.canvas.place(
            x=int(self.LEFT_COL_W * 0.2),
            y=self.TOP_MARGIN + self.TOP_OFFSET
        )

        self.level_marks = []
        steps = 10
        step_px = (self.scale_bottom - self.scale_top) / steps

        for i in range(steps + 1):
            y = self.scale_bottom - i * step_px
            color = "red" if i >= 8 else "black"

            self.canvas.create_text(
                int(canvas_w * 0.25),
                y,
                text=str(i),
                anchor="e",
                font=("Courier", 8),
                fill=color
            )

            self.level_marks.append(
                self.canvas.create_line(
                    int(canvas_w * 0.35),
                    y,
                    int(canvas_w * 0.95),
                    y,
                    fill=color
                )
            )

        # вода
        self.water_rect = self.canvas.create_rectangle(
            self.water_x1,
            self.scale_bottom,
            self.water_x2,
            self.scale_bottom,
            fill="blue",
            outline=""
        )

    # ===== GALETTE =====
    # def create_galette(self):
    #     frame_w = int(self.RIGHT_COL_W * 0.6)
    #     frame_h = int(self.height * 0.45)
    #
    #     self.galette_frame = tk.Frame(
    #         self,
    #         bg="#C0D0E0",
    #         bd=2,
    #         relief="sunken"
    #     )
    #     self.galette_frame.place(
    #         x=self.CENTER_X - frame_w // 2,
    #         y=self.TOP_MARGIN + self.TOP_OFFSET,
    #         width=frame_w,
    #         height=frame_h
    #     )
    #
    #     # подписи min/max
    #     tk.Label(self.galette_frame, text="min", bg="#C0D0E0").place(x=10, y=frame_h - 30)
    #     tk.Label(self.galette_frame, text="max", bg="#C0D0E0").place(x=frame_w - 40, y=frame_h - 30)
    #
    #     # кнопки галетки
    #     self.galette_buttons = []
    #     step = frame_w // 12
    #     for i in range(1, 12):
    #         btn = tk.Label(
    #             self.galette_frame,
    #             text=str(i),
    #             width=2,
    #             bg=WIN_LIGHT,
    #             bd=2,
    #             relief="raised",
    #         )
    #         btn.place(x=step * i - 10, y=frame_h - 70)
    #         btn.bind("<Button-1>", lambda e, idx=i: self.set_galette(idx))
    #         self.galette_buttons.append(btn)

    # def set_galette(self, idx):
    #     if self.controls_locked:
    #         return
    #
    #     self.app.on_galette_change(idx)
    #
    #     for i, b in enumerate(self.galette_buttons):
    #         b.config(bg="red" if i + 1 == idx else WIN_LIGHT)

    # ===== BOTTOM INFO =====
    def create_bottom_labels(self):
        base_y = self.height - self.BOTTOM_MARGIN

        self.status_label = tk.Label(self, bg="#A0C0E0", font=FONT_NORMAL)
        self.pos_label = tk.Label(self, bg="#A0C0E0", font=FONT_NORMAL)
        self.stage_label = tk.Label(self, bg="#A0C0E0", font=FONT_NORMAL, fg="yellow")

        self.status_label.place(x=20, y=base_y)
        self.pos_label.place(x=20, y=base_y + 22)
        self.stage_label.place(x=20, y=base_y + 44)

        self.date_label = tk.Label(
            self,
            text="18.09.2018",
            bg="#A0C0E0",
            font=FONT_NORMAL
        )
        self.date_label.place(x=self.width - 150, y=self.height - 30)

        self.alarm_label = tk.Label(
            self,
            text="АВАРИЙНАЯ ОСТАНОВКА",
            bg="red",
            fg="white",
            bd=2,
            relief="raised",
            font=FONT_NORMAL
        )

    def create_galette(self):
        frame_w = int(self.RIGHT_COL_W * 0.6)
        frame_h = int(self.height * 0.45)

        self.galette_frame = tk.Frame(
            self,
            bg="#C0D0E0",
            bd=2,
            relief="sunken"
        )
        self.galette_frame.place(
            x=self.CENTER_X - frame_w // 2,
            y=self.TOP_MARGIN + self.TOP_OFFSET,
            width=frame_w,
            height=frame_h
        )

        # подписи min/max
        tk.Label(self.galette_frame, text="min", bg="#C0D0E0").place(x=10, y=frame_h - 30)
        tk.Label(self.galette_frame, text="max", bg="#C0D0E0").place(x=frame_w - 40, y=frame_h - 30)
        # Canvas для галетки
        size = 200
        self.galette_canvas = tk.Canvas(self.galette_frame, width=size, height=size, bg="#C0D0E0", highlightthickness=0)
        self.galette_canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.galette_center = size // 2
        self.galette_radius = size // 2 - 20
        self.num_positions = 11

        # Рисуем окружность
        self.galette_canvas.create_oval(
            10, 10, size - 10, size - 10,
            fill=WIN_LIGHT,
            outline="black",
            width=2
        )

        # Рисуем цифры вокруг
        self.galette_labels = []
        for i in range(self.num_positions):
            angle = 2 * math.pi * i / self.num_positions - math.pi / 2
            x = self.galette_center + math.cos(angle) * (self.galette_radius + 16)
            y = self.galette_center + math.sin(angle) * (self.galette_radius + 16)
            lbl = self.galette_canvas.create_text(x, y, text=str(i + 1), font=FONT_NORMAL, fill="black")
            self.galette_labels.append(lbl)

        # Индикатор текущей позиции
        self.galette_marker = self.galette_canvas.create_line(
            self.galette_center, self.galette_center,
            self.galette_center, 20,
            fill="red", width=3
        )

        # Клик по Canvas
        self.galette_canvas.bind("<Button-1>", self.click_galette)

    def set_galette(self, idx):
        # Обновляем состояние через app
        if self.controls_locked:
            return
        self.app.on_galette_change(idx)
        self.update_galette_marker(idx)

    def update_galette_marker(self, idx):
        angle = 2 * math.pi * (idx - 1) / self.num_positions - math.pi / 2
        x = self.galette_center + math.cos(angle) * self.galette_radius
        y = self.galette_center + math.sin(angle) * self.galette_radius
        self.galette_canvas.coords(self.galette_marker, self.galette_center, self.galette_center, x, y)

    def click_galette(self, event):
        # Определяем, на какой сектор кликнули
        dx = event.x - self.galette_center
        dy = event.y - self.galette_center
        angle = math.atan2(dy, dx) + math.pi / 2
        if angle < 0:
            angle += 2 * math.pi
        idx = int(angle / (2 * math.pi) * self.num_positions) + 1
        self.set_galette(idx)

    # ===== UPDATE =====
    def schedule_update(self):
        if not self.alive:
            return

        self.state.update_movement()

        if self.state.level_running and not self.state.alarm_mode:
            self.state.increase_levels(STEP_AMOUNT)
        elif self.state.alarm_mode:
            self.state.increase_alarm_level()

        self.update_panel()
        self.after(100, self.schedule_update)

    # ===== UPDATE =====
    def update_panel(self):
        ratio = max(self.state.tanks) / LEVEL_MAX
        water_h = int((self.scale_bottom - self.scale_top) * ratio)

        self.canvas.coords(
            self.water_rect,
            self.water_x1,
            self.scale_bottom - water_h,
            self.water_x2,
            self.scale_bottom
        )
        state = ""
        if self.state.moving:
            state = "Движение"
        elif self.state.stage_index >= len(RECOMMENDED_POSITIONS):
            state = "Ошибка"
        else:
            state = "Останов"
        self.status_label.config(
            text="Состояние: " + state
        )
        self.pos_label.config(text=f"Текущее положение: {self.state.current_position}")

        if self.state.stage_index < len(RECOMMENDED_POSITIONS):
            next_pos = RECOMMENDED_POSITIONS[self.state.stage_index]
        else:
            next_pos = FINAL_POSITION

        self.stage_label.config(text=f"Рекомендуемое положение: {next_pos}")

        # === ALARM ===
        if self.state.alarm_triggered and not self.alarm_fired:
            self.alarm_fired = True
            self.controls_locked = True
            self.alarm_label.place(
                x=self.CENTER_X - 120,
                y=self.height - self.BOTTOM_MARGIN + 10,
                width=240,
                height=30
            )
            self.show_alarm_frame()

        # Мигаем текст тревоги
        if self.alarm_fired:
            self.alarm_visible = not self.alarm_visible
            self.alarm_label.config(fg="white" if self.alarm_visible else "red")


    def fire_final_alarm(self):
        self.alive = False
        if self.on_alarm:
            self.on_alarm()

    def show_alarm_frame(self):
        if hasattr(self, "alarm_window"):
            return

        def on_close_alarm():
            self.alive = False
            if self.on_exit:
                self.on_exit()

        from control_panel.alarm import AlarmWindow
        self.alarm_window = AlarmWindow(
            self,
            text="КРИТИЧЕСКИЙ УРОВЕНЬ ВОДЫ",
            on_close=on_close_alarm
        )
        self.alarm_window.place(
            x=self.width // 2 - 150,
            y=self.height // 2 - 75,
            width=300,
            height=150
        )


