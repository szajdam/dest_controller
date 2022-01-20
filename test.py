import time
from display import display
from temperature import temperature_reader_factory
from temperature_reader import convert_to_string

display.start()
temp_reader_keg = temperature_reader_factory.get_temp_reader_for_keg()
temp_reader_col = temperature_reader_factory.get_temp_reader_for_column()
temp_reader_cool = temperature_reader_factory.get_temp_reader_for_cooler()

while True:
    temperature_keg = convert_to_string(temp_reader_keg.get_temperature())
    temperature_col = convert_to_string(temp_reader_col.get_temperature_for_string())
    temperature_cool = convert_to_string(temp_reader_cool.get_temperature_for_string())
    display.set_values(temperature_keg, temperature_col, temperature_cool)
    time.sleep_ms(1000)
