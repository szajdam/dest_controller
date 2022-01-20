import temperature_reader

_PORT_KEG = 27
_PORT_COL = 26
_PORT_COOL = 25


def get_temp_reader_for(port_number):
    temp_reader = temperature_reader.TempReader(port_number)
    return temp_reader


def get_temp_reader_for_keg():
    return get_temp_reader_for(_PORT_KEG)


def get_temp_reader_for_column():
    return get_temp_reader_for(_PORT_COL)


def get_temp_reader_for_cooler():
    return get_temp_reader_for(_PORT_COOL)
