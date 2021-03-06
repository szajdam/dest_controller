from machine import Pin, I2C
import sh1106

import cooling_pump_controller
import temperature_reader
import time

_KEG_TEXT = 'Keg'
_KOL_TEXT = 'Kolumna'
_COOL_TEXT = 'Chlodnica'

_KEG_Y = 4
_KOL_Y = 14
_COOL_Y = 24

_TEXT_X = 2
_VALUE_X = 82

_SCREEN_Y_SIZE = 64
_SCREEN_X_SIZE = 128

_FRAME_X = _SCREEN_X_SIZE - 2
_FRAME_Y = _SCREEN_Y_SIZE - 2

_MIN_PAUSE_MS = 100


def _none_or_differs(prev_temp, current_temp):
    if prev_temp is None or prev_temp != current_temp:
        return True
    else:
        return False


def _calculate_animation_pause(pump_speed):
    if pump_speed == 0:
        return 100000
    else:
        return round(_MIN_PAUSE_MS / pump_speed / 1000)


class Display:
    __monostate = None

    def __init__(self):
        if not Display.__monostate:
            Display.__monostate = self.__dict__
            self.prev_keg = None
            self.prev_kol = None
            self.prev_cool = None

            i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
            self.display = sh1106.SH1106_I2C(_SCREEN_X_SIZE, _SCREEN_Y_SIZE, i2c)
            self.start()
        else:
            self.__dict__ = Display.__monostate

    def start(self):
        self._build_screen()
        self._set_values('--.--', '--.--', '--.--')

    def _build_screen(self):
        self.display.sleep(False)
        self.display.fill(0)
        self.display.text(_KEG_TEXT, _TEXT_X, _KEG_Y, 1)
        self.display.text(_KOL_TEXT, _TEXT_X, _KOL_Y, 1)
        self.display.text(_COOL_TEXT, _TEXT_X, _COOL_Y, 1)
        self.display.rect(1, 1, _FRAME_X, _FRAME_Y, 1)
        self.display.show()

    def update_values(self):
        temp_reader = temperature_reader.TempReader()
        keg = temp_reader.get_keg_temperature_for_string()
        kol = temp_reader.get_col_temperature_for_string()
        cool = temp_reader.get_cool_temperature_for_string()
        if self._should_update_temps(keg, kol, cool):
            self._set_values(keg, kol, cool)

    def animate_pump(self):
        pump = cooling_pump_controller.PumpControl
        cycles = 0
        while True:
            pause_ms = _MIN_PAUSE_MS
            cycles = cycles + 1
            if cycles > 10:
                pause_ms = _calculate_animation_pause(pump.get_current_speed())
                cycles = 0
            self.print_plus(1)
            time.sleep_ms(pause_ms)
            self.print_plus(0)
            self.print_x(1)
            time.sleep_ms(pause_ms)
            self.print_x(0)

    def print_plus(self, colour):
        x1 = 10
        y1 = 44
        x2 = 10
        y2 = 54
        # vertical
        self.display.line(x1, y1, x2, y2, colour)
        x1 = 5
        y1 = 49
        x2 = 15
        y2 = 49
        # horizontal
        self.display.line(x1, y1, x2, y2, colour)
        self.display.show()

    def print_x(self, colour):
        x1 = 14
        y1 = 45
        x2 = 6
        y2 = 53
        # vertical
        self.display.line(x1, y1, x2, y2, colour)
        x1 = 6
        y1 = 45
        x2 = 14
        y2 = 53
        # horizontal
        self.display.line(x1, y1, x2, y2, colour)
        self.display.show()

    def _set_values(self, keg, kol, cool):
        self.clean_temp(True)
        self.display.text(keg, _VALUE_X, _KEG_Y, 1)
        self.display.text(kol, _VALUE_X, _KOL_Y, 1)
        self.display.text(cool, _VALUE_X, _COOL_Y, 1)
        self.display.show()

    def _should_update_temps(self, keg, kol, cool):
        if _none_or_differs(self.prev_keg, keg) \
                or _none_or_differs(self.prev_kol, kol) \
                or _none_or_differs(self.prev_cool, cool):
            self.prev_keg = keg
            self.prev_kol = kol
            self.prev_cool = cool
            return True
        else:
            return False

    def clean_temp(self, should_show):
        self.display.fill_rect(_VALUE_X, _KEG_Y, _FRAME_X - _VALUE_X, _COOL_Y - _KEG_Y + 10, 0)
        if should_show:
            self.display.show()
