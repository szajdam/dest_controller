import machine
import onewire
import ds18x20


class TempReader:
    def __init__(self):
        pin = machine.Pin(27)
        self.ds = ds18x20.DS18X20(onewire.OneWire(pin))
        self.roms = self.ds.scan()
        print('found devices:', self.roms)

    def read_temperature(self):
        self.ds.convert_temp()
        temperature = None
        for rom in self.roms:
            temperature = self.ds.read_temp(rom);
        return temperature