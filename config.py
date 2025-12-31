# ====== ОБЩИЕ НАСТРОЙКИ ======

APP_TITLE = "RPI Quest Control"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


# ====== ЭКРАН ЗАГРУЗКИ ======

BOOT_DURATION_MS = 8000  # 8 секунд всего
BOOT_STEPS = 100          # 100 шагов
STEP_DELAY = BOOT_DURATION_MS // BOOT_STEPS  # миллисекунды
STEP_AMOUNT = 10


# ====== ПАРОЛИ ======

PLAYER_PASSWORD = "2018"
OPERATOR_PASSWORD = "4848"

# ====== УРОВЕНЬ ВОДЫ ======

LEVEL_MIN = 0
LEVEL_MAX = 1000
ALARM_LEVEL_MAX = 3000
FAST_STEP = 150
FAST_RISE_INTERVAL = 100  # мс
LEVEL_ALARM = 1300

LEVEL_RISE_INTERVAL = 40     # мс (10 секунд)
LEVEL_DROP_TIME = 2_000          # мс (3 секунды)
ALARM_DELAY = 1_000               # мс (5 секунд)

# ====== РЕКОМЕНДОВАННЫЕ ПОЛОЖЕНИЯ ГАЛЕТНИКА ======

RECOMMENDED_POSITIONS = [4, 8]
FINAL_POSITION = 11


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
