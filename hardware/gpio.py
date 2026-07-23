import sys

if sys.platform == "linux":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    USING_REAL_GPIO = True
else:
    # ПК — эмуляция
    USING_REAL_GPIO = False

class Galette:
    def __init__(self, pins):
        self.pins = pins
        if USING_REAL_GPIO:
            for p in pins:
                GPIO.setup(p, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        else:
            # Эмуляция: текущее положение
            self.current = 1

    def get_position(self):
        if USING_REAL_GPIO:
            for i, p in enumerate(self.pins, 1):
                if GPIO.input(p) == GPIO.LOW:
                    return i
        else:
            return self.current

    def set_mock_position(self, pos):
        if not USING_REAL_GPIO:
            self.current = self.current

class Projector:
    def __init__(self, input_pin, relay_pin):
        self.input_pin = input_pin
        self.relay_pin = relay_pin
        if USING_REAL_GPIO:
            GPIO.setup(input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(relay_pin, GPIO.OUT)
        else:
            self.state = False

    def is_on(self):
        if USING_REAL_GPIO:
            return GPIO.input(self.input_pin) == GPIO.LOW
        else:
            return self.state

    def turn_on_relay(self):
        if USING_REAL_GPIO:
            GPIO.output(self.relay_pin, GPIO.HIGH)
        else:
            self.state = True

    def turn_off_relay(self):
        if USING_REAL_GPIO:
            GPIO.output(self.relay_pin, GPIO.LOW)
        else:
            self.state = False
