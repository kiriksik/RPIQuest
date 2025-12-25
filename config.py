# ====== ОБЩИЕ НАСТРОЙКИ ======

APP_TITLE = "RPI Quest Control"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000


# ====== ЭКРАН ЗАГРУЗКИ ======

BOOT_DURATION_MS = 8000  # 8 секунд всего
BOOT_STEPS = 100          # 100 шагов
STEP_DELAY = BOOT_DURATION_MS // BOOT_STEPS  # миллисекунды
STEP_AMOUNT = 1


# ====== ПАРОЛИ ======

PLAYER_PASSWORD = "2018"
OPERATOR_PASSWORD = "4848"

# ====== УРОВЕНЬ ВОДЫ ======

LEVEL_MIN = 500
LEVEL_MAX = 2000
LEVEL_ALARM = 3000
ALARM_DELAY = 5000      # 5 секунд
FAST_RISE_INTERVAL = 500  # быстрый рост воды (0.5 сек)
FAST_RISE_STEP = 200


LEVEL_RISE_INTERVAL = 1_000     # мс (10 секунд)
LEVEL_DROP_TIME = 2_000          # мс (3 секунды)
ALARM_DELAY = 1_000               # мс (5 секунд)

# ====== РЕКОМЕНДОВАННЫЕ ПОЛОЖЕНИЯ ГАЛЕТНИКА ======

RECOMMENDED_POSITIONS = [4, 8, 11]

# ====== GPIO (для Raspberry Pi) ======

GALETTE_PINS = {
    1: 5,
    2: 6,
    3: 13,
    4: 19,
    5: 26,
    6: 12,
    7: 16,
    8: 20,
    9: 21,
    10: 25,
    11: 24
}

PROJECTOR_INPUT_PIN = 18
PROJECTOR_RELAY_PIN = 23

# ====== СЕРВЕР ======

SERVER_URL = "http://localhost:8000"

# ====== ТЕКСТ В БЛОКНОТЕ ======

STORY_TEXT = (
    "Привет.\n\n"
    "Проектор, который мы нашли, показывает что-то непонятное:\n"
    "вроде план нашего пункта управления, но какой-то другой.\n\n"
    "Наше здание было построено 94 года назад,\n"
    "после последнего крупного наводнения.\n\n"
    "Возможно, раньше было именно так."
)
