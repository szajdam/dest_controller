from machine import Timer
import temperature_reader
import display

disp = display.Display()
disp.start()
Timer.Alarm(disp.set_values, 1, Timer.PERIODIC)

temp_reader = temperature_reader.TempReader()
Timer.Alarm(temp_reader.read_temperatures, 1, Timer.PERIODIC)
