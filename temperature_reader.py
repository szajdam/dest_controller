import machine
import onewire
import ds18x20
import time
from threading import Lock, Thread

_PORT_KEG = 27

_PORT_COL = 26

_PORT_COOL = 25

_REFRESH_DELAY = 1


def _convert_to_string(temp_decimal):
    try:
        return "{:.2f}".format(temp_decimal)
    except ValueError:
        return '-.--'


class MeasureResult:
    def __init__(self, temperature_keg, temperature_column, temperature_cooler):
        self.temperature_keg = temperature_keg
        self.temperature_column = temperature_column
        self.temperature_cooler = temperature_cooler


class TempSensor:

    def __init__(self, port_number):
        self.sensor = None
        self.last_time = None
        self.is_initialised = False
        self.port = port_number
        pin = machine.Pin(port_number)
        onewire_port = onewire.OneWire(pin)
        self.ds = ds18x20.DS18X20(onewire_port)
        self.check_sensor_availability()

    def check_sensor_availability(self):
        sensors = self.ds.scan()
        print('Found devices:', sensors, 'on port', self.port)
        if len(sensors) > 0:
            self.is_initialised = True
            self.sensor = sensors[0]
        else:
            self.is_initialised = False

    def read_temperature(self):
        try:
            if self.is_initialised:
                self.ds.convert_temp()
                temperature = self.ds.read_temp(self.sensor)
                print('Measured :', _convert_to_string(temperature), 'on port', self.port)
                return temperature
            else:
                self.check_sensor_availability()
                return 0.00
        except onewire.OneWireError:
            self.check_sensor_availability()


class TempReaderSingletonMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class TempReader(metaclass=TempReaderSingletonMeta):

    def __init__(self):
        self.sensor_keg = TempSensor(_PORT_KEG)
        self.sensor_column = TempSensor(_PORT_COL)
        self.sensor_cooler = TempSensor(_PORT_COOL)
        self.last_time = time.time()
        self.measured_result = MeasureResult(0.00, 0.00, 0.00)

    def get_keg_temperature_for_string(self):
        return _convert_to_string(self.get_keg_temperature())

    def get_keg_temperature(self):
        self.read_temperatures()
        return self.measured_result.temperature_keg

    def get_col_temperature_for_string(self):
        return _convert_to_string(self.get_col_temperature())

    def get_col_temperature(self):
        self.read_temperatures()
        return self.measured_result.temperature_column

    def get_cool_temperature_for_string(self):
        return _convert_to_string(self.get_cool_temperature())

    def get_cool_temperature(self):
        self.read_temperatures()
        return self.measured_result.temperature_cooler

    def read_temperatures(self):
        current_time = time.time()
        print('TimeDiff', current_time - self.last_time)
        if current_time - self.last_time > _REFRESH_DELAY:
            temperature_keg = self.sensor_keg.read_temperature()
            temperature_column = self.sensor_column.read_temperature()
            temperature_cooler = self.sensor_cooler.read_temperature()
            print('Keg reading', _convert_to_string(temperature_keg))
            print('Col reading', _convert_to_string(temperature_column))
            print('Cool reading', _convert_to_string(temperature_cooler))
            self.measured_result = MeasureResult(temperature_keg, temperature_column, temperature_cooler)
            self.last_time = current_time
