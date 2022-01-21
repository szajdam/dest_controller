import time

import temperature_reader
import display

_REFRESH_DELAY = 1000

prev_temperature_keg = "0.00"
prev_temperature_col = "0.00"
prev_temperature_cool = "0.00"

disp = display.Display()
disp.start()
temp_reader_keg = temperature_reader.TempReader()
temp_reader_col = temperature_reader.TempReader()
temp_reader_cool = temperature_reader.TempReader()

while True:
    temperature_keg = temp_reader_keg.get_keg_temperature_for_string()
    print("Prev " + prev_temperature_keg + " New" + temperature_keg)
    print(temperature_keg != prev_temperature_keg)
    temperature_col = temp_reader_col.get_col_temperature_for_string()
    print("Prev " + prev_temperature_col + " New" + temperature_col)
    print(temperature_col != prev_temperature_col)
    temperature_cool = temp_reader_cool.get_cool_temperature_for_string()
    print("Prev " + prev_temperature_cool + " New" + temperature_cool)
    print(temperature_cool != prev_temperature_cool)
    if temperature_keg != prev_temperature_keg \
            or temperature_col != prev_temperature_col \
            or temperature_cool != prev_temperature_cool:
        disp.set_values(temperature_keg, temperature_col, temperature_cool)
        prev_temperature_keg = temperature_keg
        prev_temperature_col = temperature_col
        prev_temperature_cool = temperature_cool
    time.sleep_ms(_REFRESH_DELAY)
