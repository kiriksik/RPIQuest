import threading
import time

USING_REAL_GPIO = True

USING_REAL_GPIO = False
GPIO = None


try:
    import RPi.GPIO as GPIO

    GPIO.setmode(GPIO.BCM)

    USING_REAL_GPIO = True

    print("REAL GPIO MODE")


except ImportError:

    print("GPIO MOCK MODE")

class GPIOController:
    def __init__(
        self,
        galette_pins,        # list из 11 пинов
        projector_input_pin, # input_pullup
        projector_relay_pin, # output
        on_galette_change=None,
        on_projector_on=None,
        on_projector_off=None,
    ):
        self.galette_pins = galette_pins
        self.projector_input_pin = projector_input_pin
        self.projector_relay_pin = projector_relay_pin

        self.on_galette_change = on_galette_change
        self.on_projector_on = on_projector_on
        self.on_projector_off = on_projector_off

        self.last_position = None
        self.last_projector_state = None

        if USING_REAL_GPIO:
            self._setup_gpio()

        self.running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()

    # ---------- GPIO SETUP ----------
    def _setup_gpio(self):
        for pin in self.galette_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.setup(self.projector_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.projector_relay_pin, GPIO.OUT)
        GPIO.output(self.projector_relay_pin, GPIO.LOW)

    # ---------- POLLING ----------
    def _poll_loop(self):
        while self.running:
            self._check_galette()
            self._check_projector()
            time.sleep(0.05)

    def _check_galette(self):
        pos = self.get_galette_position()
        if pos and pos != self.last_position:
            self.last_position = pos
            if self.on_galette_change:
                self.on_galette_change(pos)

    def _check_projector(self):
        state = self.is_projector_on()
        if state != self.last_projector_state:
            self.last_projector_state = state
            if state:
                self.turn_relay_on()
                if self.on_projector_on:
                    self.on_projector_on()
            else:
                self.turn_relay_off()
                if self.on_projector_off:
                    self.on_projector_off()

    # ---------- READERS ----------
    def get_galette_position(self):
        if USING_REAL_GPIO:
            for idx, pin in enumerate(self.galette_pins, start=1):
                if GPIO.input(pin) == GPIO.LOW:
                    return idx
        return None

    def is_projector_on(self):
        if USING_REAL_GPIO:
            return GPIO.input(self.projector_input_pin) == GPIO.LOW
        return False

    # ---------- RELAY ----------
    def turn_relay_on(self):
        if USING_REAL_GPIO:
            GPIO.output(self.projector_relay_pin, GPIO.HIGH)

    def turn_relay_off(self):
        if USING_REAL_GPIO:
            GPIO.output(self.projector_relay_pin, GPIO.LOW)

    # ---------- CLEANUP ----------
    def stop(self):
        self.running = False
        if USING_REAL_GPIO:
            GPIO.cleanup()

    def cleanup(self):
        if USING_REAL_GPIO:
            GPIO.cleanup()


