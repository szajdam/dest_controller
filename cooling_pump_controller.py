from machine import Pin, PWM

_IN2_PIN_NUMBER = 27

_IN1_PIN_NUMBER = 26

_PWM_PIN_NUMBER = 25


def get_duty(percentage):
    return percentage / 100 * 65535


class PumpControl:
    def __init__(self):
        pin_pwm = Pin(_PWM_PIN_NUMBER)  # IO25/D2
        self.pin_in1 = Pin(_IN1_PIN_NUMBER, Pin.OUT)  # IO26/D3
        self.pin_in2 = Pin(_IN2_PIN_NUMBER, Pin.OUT)  # IO27/D4

        self.pwm = PWM(pin_pwm, freq=1000)
        self.pwm.duty_u16(get_duty(0))  # current duty cycle, range 0-65535

        self.pin_in1.off()
        self.pin_in2.on()

    def change_speed(self, percentage):
        self.pwm.duty_u16(get_duty(percentage))

    def start(self):
        self.pwm.duty_u16(get_duty(100))
        self.pin_in1.off()
        self.pin_in2.on()

    def stop(self):
        self.pwm.duty_u16(get_duty(0))

    def fast_stop(self):
        self.pin_in1.on()
        self.pin_in2.on()
