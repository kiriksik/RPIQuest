from config import (
    LEVEL_MIN,
    LEVEL_MAX,
    RECOMMENDED_POSITIONS,
)
from config import LEVEL_ALARM, ALARM_DELAY, FAST_RISE_INTERVAL


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.started = False
        self.password_ok = False

        self.level = LEVEL_MIN
        self.level_running = False

        self.stage_index = 0
        self.current_position = 1

        self.alarm_mode = False
        self.alarm_triggered = False

    def start_pc(self):
        self.started = True

    def check_password(self, password: str) -> bool:
        if password == "2018":
            self.password_ok = True
            self.level_running = True
            return True
        return False

    def increase_level(self, step=100, max_level=LEVEL_MAX):
        if not self.level_running:
            return

        if self.level < max_level:
            self.level += step
            if self.level > max_level:
                self.level = max_level

    # ====== ГАЛЕТНИК ======

    def set_galette_position(self, pos: int):
        self.current_position = pos

        if self.stage_index >= len(RECOMMENDED_POSITIONS):
            return

        required = RECOMMENDED_POSITIONS[self.stage_index]

        if pos == required and self.level >= LEVEL_MAX:
            self.on_correct_position()

    def on_correct_position(self):
        self.level = LEVEL_MIN
        self.stage_index += 1

        # если это была позиция 11 — запускаем аварию
        if self.stage_index >= len(RECOMMENDED_POSITIONS):
            self.start_alarm()

    # ====== АВАРИЯ ======

    def start_alarm(self):
        self.alarm_mode = True
        self.level_running = True

    def increase_alarm_level(self):
        if not self.alarm_mode:
            return

        if self.level < LEVEL_ALARM:
            self.level += 200
            if self.level >= LEVEL_ALARM:
                self.level = LEVEL_ALARM
                self.alarm_triggered = True
