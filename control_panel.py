import tkinter as tk
from styles import WIN_BG, WIN_DARK, WIN_LIGHT, WIN_BLACK, DESKTOP_BG, TITLE_BG_ACTIVE, TITLE_FG, FONT_NORMAL, FONT_TITLE, FONT_BIG
from widgets import WinButton
from game_logic import GameState
from config import LEVEL_MAX, RECOMMENDED_POSITIONS, LEVEL_RISE_INTERVAL, ALARM_DELAY, FAST_RISE_INTERVAL, SCREEN_HEIGHT, SCREEN_WIDTH

class ControlPanel(tk.Frame):
    def __init__(self, parent, state: GameState, on_alarm=None):
        super().__init__(parent, bg="#A0C0E0", bd=2, relief="sunken")

        self.state = state
        self.on_alarm = on_alarm
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
            int(canvas_w * 0.45),
            self.scale_bottom,
            int(canvas_w * 0.65),
            self.scale_bottom,
            fill="blue",
            outline=""
        )

    # ===== GALETTE =====
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

        # кнопки галетки
        self.galette_buttons = []
        step = frame_w // 12
        for i in range(1, 12):
            btn = tk.Label(
                self.galette_frame,
                text=str(i),
                width=2,
                bg=WIN_LIGHT,
                bd=2,
                relief="raised",
            )
            btn.place(x=step * i - 10, y=frame_h - 70)
            btn.bind("<Button-1>", lambda e, idx=i: self.set_galette(idx))
            self.galette_buttons.append(btn)

    def set_galette(self, idx):
        if self.controls_locked:
            return
        self.state.set_galette_position(idx)
        for i, b in enumerate(self.galette_buttons):
            b.config(bg="red" if i + 1 == idx else WIN_LIGHT)

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

    # ===== UPDATE =====
    def schedule_update(self):
        if not self.alive:
            return

        if self.state.alarm_mode:
            self.state.increase_alarm_level()
        else:
            self.state.increase_levels()

        self.update_panel()
        self.after(100, self.schedule_update)

    def update_panel(self):
        ratio = max(self.state.tanks) / LEVEL_MAX
        water_h = int((self.scale_bottom - self.scale_top) * ratio)

        self.canvas.update_idletasks()  # чтобы получить реальную ширину
        cw = self.canvas.winfo_width()

        self.canvas.coords(
            self.water_rect,
            cw * 0.45,
            self.scale_bottom - water_h,
            cw * 0.65,
            self.scale_bottom
        )


        self.status_label.config(
            text="Состояние: " + ("Движение" if self.state.level_running else "Останов")
        )
        self.pos_label.config(text=f"Текущее положение: {self.state.current_position}")

        if self.state.stage_index < len(RECOMMENDED_POSITIONS):
            self.stage_label.config(
                text=f"Рекомендуемое положение: {RECOMMENDED_POSITIONS[self.state.stage_index]}"
            )

        if self.state.alarm_triggered:
            if not self.alarm_fired:
                self.alarm_fired = True
                self.controls_locked = True
                self.alarm_label.place(
                    x=self.CENTER_X - 120,
                    y=self.height - self.BOTTOM_MARGIN + 10,
                    width=240,
                    height=30
                )
                self.after(ALARM_DELAY, self.fire_final_alarm)

            self.alarm_visible = not self.alarm_visible
            self.alarm_label.config(fg="white" if self.alarm_visible else "red")

    def fire_final_alarm(self):
        self.alive = False
        if self.on_alarm:
            self.on_alarm()
