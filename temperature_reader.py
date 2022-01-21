import machine
import onewire
import ds18x20
import time

_PORT_KEG = 27

_PORT_COL = 26

_PORT_COOL = 25

_REFRESH_DELAY = 1000


def convert_to_string(temp_decimal)
    return "{:.2f}".format(temp_decimal)


class MeasureResult:
    def __init__(self):
        self.temperature_keg = None
        self.temperature_column = None
        self.temperature_cooler = None

    def __init__(self, temperature_keg, temperature_column, temperature_cooler):
        self.temperature_keg = temperature_keg
        self.temperature_column = temperature_column
        self.temperature_cooler = temperature_cooler

    @property
    def temperature_keg(self):
        return self.temperature_keg

    @temperature_keg.setter
    def temperature_keg(self, temperature_keg):
        self.temperature_keg = temperature_keg

    @property
    def temperature_column(self):
        return self.temperature_column

    @temperature_column.setter
    def temperature_column(self, temperature_column):
        self.temperature_column = temperature_column

    @property
    def temperature_cooler(self):
        return self.temperature_cooler

    @temperature_cooler.setter
    def temperature_cooler(self, temperature_cooler):
        self.temperature_cooler = temperature_cooler


class TempSensor:
    is_initialised = False

    def __init__(self, port_number):
        self.last_time = None
        pin = machine.Pin(port_number)
        self.ds = ds18x20.DS18X20(onewire.OneWire(pin))
        sensors = self.ds.scan()
        print('found devices:', sensors)
        if len(sensors) > 0:
            self.is_initialised = True
            self.sensor = sensors[0]

    def read_temperature(self):
        if self.is_initialised:
            self.ds.convert_temp()
            temperature = self.ds.read_temp(self.sensor)
            print("Measured : " + temperature)
            return temperature
        else:
            return 0.00


class TempReader:
    last_time = None

    def __init__(self):
        self.sensor_keg = TempSensor(_PORT_KEG)
        self.sensor_column = TempSensor(_PORT_COL)
        self.sensor_cooler = TempSensor(_PORT_COOL)

        self.measure_result = MeasureResult()

    def get_keg_temperature_for_string(self):
        return "{:.2f}".format(self.get_keg_temperature())

    def get_keg_temperature(self):
        self.read_temperatures()
        return self.measure_result.temperature_keg

    def read_temperatures(self):
        current_time = time.time()
        if self.last_time is not None \
                or current_time - self.last_time > _REFRESH_DELAY:
            temperature_keg = self.sensor_keg.read_temperature()
            temperature_column = self.sensor_column.read_temperature()
            temperature_cooler = self.sensor_cooler.read_temperature()
            self.measure_result = MeasureResult(temperature_keg, temperature_column, temperature_cooler)
