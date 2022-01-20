import time
from display import display
from temperature import temperature_reader_factory
from temperature_reader import convert_to_string


_REFRESH_DELAY = 1000

prev_temperature_keg = None
prev_temperature_col = None
prev_temperature_cool = None

display.start()
temp_reader_keg = temperature_reader_factory.get_temp_reader_for_keg()
temp_reader_col = temperature_reader_factory.get_temp_reader_for_column()
temp_reader_cool = temperature_reader_factory.get_temp_reader_for_cooler()

while True:
    temperature_keg = temp_reader_keg.get_temperature()
    temperature_col = temp_reader_col.get_temperature_for_string()
    temperature_cool = temp_reader_cool.get_temperature_for_string()
    if temperature_keg != prev_temperature_keg \
            or temperature_col != prev_temperature_col \
            or temperature_cool != prev_temperature_cool:
        display.set_values(convert_to_string(temperature_keg), convert_to_string(temperature_col),
                           convert_to_string(temperature_cool))
        prev_temperature_keg = temperature_keg
        prev_temperature_col = temperature_col
        prev_temperature_cool = temperature_cool
    time.sleep_ms(_REFRESH_DELAY)
