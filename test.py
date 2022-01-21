import time

import temperature_reader
import display

_REFRESH_DELAY = 1000

prev_temperature_keg = None
prev_temperature_col = None
prev_temperature_cool = None

display.start()
temp_reader_keg = temperature_reader.TempReader
temp_reader_col = temperature_reader.TempReader
temp_reader_cool = temperature_reader.TempReader

while True:
    temperature_keg = temp_reader_keg.get_keg_temperature_for_string()
    temperature_col = temp_reader_col.get_keg_temperature_for_string()
    temperature_cool = temp_reader_cool.get_keg_temperature_for_string()
    if temperature_keg != prev_temperature_keg \
            or temperature_col != prev_temperature_col \
            or temperature_cool != prev_temperature_cool:
        display.set_values(temperature_keg, temperature_col,
                           temperature_cool)
        prev_temperature_keg = temperature_keg
        prev_temperature_col = temperature_col
        prev_temperature_cool = temperature_cool
    time.sleep_ms(_REFRESH_DELAY)
