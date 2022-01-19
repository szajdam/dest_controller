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

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
display = sh1106.SH1106_I2C(_SCREEN_X_SIZE, _SCREEN_Y_SIZE, i2c)


def start():
    build_screen();
    set_values('30.0', '30.0', '30.0');


def build_screen():
    display.sleep(False)
    display.fill(0)
    display.text(_KEG_TEXT, _TEXT_X, _KEG_Y, 1)
    display.text(_KOL_TEXT, _TEXT_X, _KOL_Y, 1)
    display.text(_COOL_TEXT, _TEXT_X, _COOL_Y, 1)
    display.rect(1, 1, _FRAME_X, _FRAME_Y, 1)
    display.show()


def set_values(keg, kol, cool):
    clean()
    display.text(keg, _VALUE_X, _KEG_Y, 1)
    display.text(kol, _VALUE_X, _KOL_Y, 1)
    display.text(cool, _VALUE_X, _COOL_Y, 1)
    display.show()


def clean():
    display.fill_rect(_VALUE_X, _KEG_Y, _FRAME_X - _VALUE_X, _COOL_Y - _KEG_Y + 10, 0)
    display.show()
