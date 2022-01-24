import display
from machine import Timer

disp = display.Display()
disp.start()

t1 = Timer(0)
t1.init(mode=Timer.PERIODIC, period=1000, callback=lambda t:disp.update_values())

# temp_reader = temperature_reader.TempReader()
# t2 = machine.Timer(2)
# t2.init(callback=temp_reader.read_temperatures, period=1, mode=machine.Timer.PERIODIC)
