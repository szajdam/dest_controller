from cooling_pump_controller import pump_control
import time

pump = pump_control()
pump.start()
time.sleep_ms(10000)
pump.stop()
time.sleep_ms(10000)
pump.start()
time.sleep_ms(10000)
pump.change_speed(50)


