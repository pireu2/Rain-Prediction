import adafruit_tsl2561
import board

def get_sensor():
    try:
        i2c = board.I2C()
        tsl = adafruit_tsl2561.TSL2561(i2c, 0x39)
    except (OSError, ValueError):
        print('TSL2561 not detected')
        return None
    return tsl