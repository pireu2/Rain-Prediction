import adafruit_tsl2561
import board
from constants.constants import TSL2561_ADDRESS


def get_sensor():
    try:
        i2c = board.I2C()
        tsl = adafruit_tsl2561.TSL2561(i2c, TSL2561_ADDRESS)
    except (OSError, ValueError, AttributeError):
        print("TSL2561 not detected")
        return None
    return tsl
