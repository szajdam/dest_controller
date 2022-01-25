from machine import Pin, PWM

import temperature_reader

_IN2_PIN_NUMBER = 27

_IN1_PIN_NUMBER = 26

_PWM_PIN_NUMBER = 25

_COOL_TEMP_HIGH = 35.0
_COOL_TEMP_LOW = 25.0

_SPEED_ADJUST_VALUE = 5


def get_duty(percentage) -> int:
    return round(percentage / 100 * 1023)


def is_higher(temperature):
    return temperature >= _COOL_TEMP_HIGH


def is_lower(temperature):
    return temperature < _COOL_TEMP_LOW


class PumpControlSingleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance


class PumpControl(PumpControlSingleton):
    _current_speed = get_duty(0)

    def __init__(self):
        pin_pwm = Pin(_PWM_PIN_NUMBER)  # IO25/D2
        self.pin_in1 = Pin(_IN1_PIN_NUMBER, Pin.OUT)  # IO26/D3
        self.pin_in2 = Pin(_IN2_PIN_NUMBER, Pin.OUT)  # IO27/D4

        self.pwm = PWM(pin_pwm, freq=1000)
        self.pwm.duty(get_duty(0))  # current duty cycle, range 0-65535

        self.pin_in1.off()
        self.pin_in2.on()

    def adjust_speed(self):
        temp_reader = temperature_reader.TempReader()
        cool_temp = temp_reader.get_cool_temperature_for_string()
        if is_higher(cool_temp):
            new_speed = self._current_speed + _SPEED_ADJUST_VALUE
            self.change_speed(new_speed)
        if is_lower(cool_temp):
            new_speed = self._current_speed - _SPEED_ADJUST_VALUE
            self.change_speed(new_speed)

    def change_speed(self, percentage):
        self.pwm.duty(get_duty(percentage))
        self._current_speed = percentage
        print('Pump speed adjusted to', percentage)

    def start(self):
        self.pwm.duty(get_duty(100))
        self.pin_in1.off()
        self.pin_in2.on()

    def stop(self):
        self.pwm.duty(get_duty(0))

    def fast_stop(self):
        self.pin_in1.on()
        self.pin_in2.on()

    def is_running(self):
        return self._current_speed > 0
