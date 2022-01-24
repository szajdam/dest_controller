import display
import cooling_pump_controller
from machine import Timer

disp = display.Display()
disp.start()

t1 = Timer(0)
t1.init(mode=Timer.PERIODIC, period=1000, callback=lambda t: disp.update_values())

pump_controller = cooling_pump_controller.PumpControl()
t2 = Timer(1)
t2.init(mode=Timer.PERIODIC, period=5000, callback=lambda t: pump_controller.adjust_speed())
