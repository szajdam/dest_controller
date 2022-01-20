import machine
import onewire
import ds18x20


def convert_to_string(temp_decimal):
    return "{:.2f}".format(temp_decimal)


class TempReader:
    temperature = None

    def __init__(self, pin_number):
        self.temperature = 0.00
        pin = machine.Pin(pin_number)
        self.ds = ds18x20.DS18X20(onewire.OneWire(pin))
        self.roms = self.ds.scan()
        print('found devices:', self.roms)

    def get_temperature_for_string(self):
        if self.temperature is not None:
            return "{:.2f}".format(self.temperature)
        else:
            return "00.00"

    def read_temperature(self):
        if len(self.roms) > 0:
            self.ds.convert_temp()
            for rom in self.roms:
                self.temperature = self.ds.read_temp(rom);
        else:
            self.temperature = None
