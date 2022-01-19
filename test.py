import time
import display
import temperature_reader

display.start()
temp_reader = temperature_reader.TempReader()
temperature = temp_reader.read_temperature()
for i in range(100):
    temperature = "{:.2f}".format(temp_reader.read_temperature())
    display.set_values(temperature, '12.11', '12.12')
    time.sleep_ms(1000)
