from cooling_pump_controller import PumpControl
import time

pump = PumpControl()
pump.start()
time.sleep_ms(10000)
pump.stop()
time.sleep_ms(10000)
pump.start()
time.sleep_ms(10000)
pump.change_speed(50)


