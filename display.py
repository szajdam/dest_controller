from machine import Pin, I2C
import sh1106

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


class Display:
    def __init__(self):
        i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
        self.display = sh1106.SH1106_I2C(_SCREEN_X_SIZE, _SCREEN_Y_SIZE, i2c)

    def start(self):
        self.build_screen()
        self.set_values('30.0', '30.0', '30.0')

    def build_screen(self):
        self.display.sleep(False)
        self.display.fill(0)
        self.display.text(_KEG_TEXT, _TEXT_X, _KEG_Y, 1)
        self.display.text(_KOL_TEXT, _TEXT_X, _KOL_Y, 1)
        self.display.text(_COOL_TEXT, _TEXT_X, _COOL_Y, 1)
        self.display.rect(1, 1, _FRAME_X, _FRAME_Y, 1)
        self.display.show()

    def set_values(self, keg, kol, cool):
        self.clean(True)
        self.display.text(keg, _VALUE_X, _KEG_Y, 1)
        self.display.text(kol, _VALUE_X, _KOL_Y, 1)
        self.display.text(cool, _VALUE_X, _COOL_Y, 1)
        self.display.show()

    def clean(self, should_show):
        self.display.fill_rect(_VALUE_X, _KEG_Y, _FRAME_X - _VALUE_X, _COOL_Y - _KEG_Y + 10, 0)
        if should_show:
            self.display.show()
