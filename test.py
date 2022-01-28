import display
import cooling_pump_controller
from machine import Timer
import _thread


def run():
    disp = display.Display()

    t1 = Timer(0)
    t1.init(mode=Timer.PERIODIC, period=1000, callback=lambda t: disp.update_values())

    _thread.start_new_thread(disp.animate_pump, ())

    pump_controller = cooling_pump_controller.PumpControl()
    t2 = Timer(1)
    t2.init(mode=Timer.PERIODIC, period=5000, callback=lambda t: pump_controller.adjust_speed())
