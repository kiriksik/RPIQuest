from config import LEVEL_MIN, LEVEL_MAX, RECOMMENDED_POSITIONS, LEVEL_ALARM
import random

class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.started = False
        self.password_ok = False

        # 3 бака
        self.tanks = [LEVEL_MIN, LEVEL_MIN, LEVEL_MIN]

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

    # === ПЛАВНЫЙ РОСТ УРОВНЕЙ ===
    def increase_levels(self, step=20):
        if not self.level_running:
            return

        for i in range(3):
            if self.tanks[i] < LEVEL_MAX:
                self.tanks[i] += random.randint(step // 2, step)
                if self.tanks[i] > LEVEL_MAX:
                    self.tanks[i] = LEVEL_MAX

    def max_level(self):
        return max(self.tanks)

    def set_galette_position(self, pos: int):
        self.current_position = pos

        if self.stage_index >= len(RECOMMENDED_POSITIONS):
            return

        required = RECOMMENDED_POSITIONS[self.stage_index]

        # ✅ УСЛОВИЕ: ХОТЯ БЫ ОДИН БАК ПОЛОН
        if pos == required and self.max_level() >= LEVEL_MAX:
            self.on_correct_position()

    def on_correct_position(self):
        self.tanks = [LEVEL_MIN, LEVEL_MIN, LEVEL_MIN]
        self.stage_index += 1

        if self.stage_index >= len(RECOMMENDED_POSITIONS):
            self.start_alarm()

    def start_alarm(self):
        self.alarm_mode = True
        self.level_running = True

    def increase_alarm_level(self):
        if not self.alarm_mode:
            return

        for i in range(3):
            self.tanks[i] += 50
            if self.tanks[i] >= LEVEL_ALARM:
                self.tanks[i] = LEVEL_ALARM
                self.alarm_triggered = True
