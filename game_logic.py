from config import LEVEL_MIN, LEVEL_MAX, RECOMMENDED_POSITIONS, FINAL_POSITION, FAST_STEP, ALARM_LEVEL_MAX, STEP_AMOUNT
EVENT_LEVEL_MAX = "levelMax"
EVENT_LEVEL_MIN = "levelMin"
EVENT_ALARM = "alarm"
EVENT_POS = "pos"


class GameState:
    def __init__(self):
        self.reset()


    def reset(self):
        self.can_turn_galette = False
        self.started = False
        self.password_ok = False

        self.waiting_for_position = True
        self.level_timer = 0

        # 3 бака
        self.tanks = [LEVEL_MIN, LEVEL_MIN, LEVEL_MIN]

        self.level_running = False
        self.stage_index = 0
        self.current_position = 1


        self.alarm_mode = False
        self.alarm_triggered = False
        self.alarm_level = 0

        self.moving = False
        self.move_timer = 0

    def start_pc(self):
        self.started = True

    def start_level_rise(self):
        self.level_running = True

    def start_movement(self):
        self.moving = True
        self.can_turn_galette = False
        self.move_timer = 50  # 5 секунд * 10 (для таймера 0.1 с)
        self.level_running = False  # вода ещё не растёт

    def update_movement(self):
        if self.moving:
            if self.move_timer > 0:
                self.move_timer -= 1
                self.drop_levels(STEP_AMOUNT)
            else:
                self.moving = False
                self.level_running = True

    def check_password(self, password):
        if password == "2018":
            return "ok"
        if password == "4848":
            return "exit"
        return "fail"

    def start_fast_alarm_rise(self):
        self.alarm_mode = True
        self.level_running = True

    def increase_alarm_level(self):
        for i in range(3):
            self.tanks[i] = min(self.tanks[i] + FAST_STEP, ALARM_LEVEL_MAX)

        if max(self.tanks) >= ALARM_LEVEL_MAX and not self.alarm_triggered:
            self.alarm_triggered = True
            return ["alarm"]

        return []

    # === ПЛАВНЫЙ РОСТ УРОВНЕЙ ===
    def increase_levels(self, step):
        events = []

        for i in range(3):
            if not self.moving:
                self.tanks[i] = min(self.tanks[i] + step, LEVEL_MAX)

        if self.max_level() >= LEVEL_MAX and not self.can_turn_galette:
            self.can_turn_galette = True
            events.append("levelMax")

        return events

    def max_level(self):
        return max(self.tanks)

    def set_galette_position(self, pos):
        if not self.can_turn_galette:
            return {"result": "blocked", "events": []}

        self.current_position = pos
        events = []

        if self.stage_index < len(RECOMMENDED_POSITIONS):
            if pos == RECOMMENDED_POSITIONS[self.stage_index]:
                self.stage_index += 1
                events.append(f"pos{pos}")
                events.append("levelMin")

                if self.stage_index == len(RECOMMENDED_POSITIONS) and pos == FINAL_POSITION:
                    self.start_alarm()
                    events.append("alarm")
                    return {"result": "final", "events": events}

                return {"result": "correct", "events": events}

        if pos == FINAL_POSITION and self.stage_index == len(RECOMMENDED_POSITIONS):
            self.start_alarm()
            events.append("pos11")
            events.append("alarm")
            return {"result": "final", "events": events}

        return {"result": "wrong", "events": []}

    def drop_levels(self, step):
        if not self.moving:
            return
        for i in range(3):
            self.tanks[i] = max(self.tanks[i] - step, LEVEL_MIN)


    def start_alarm(self):
        self.alarm_mode = True
        self.level_running = True


