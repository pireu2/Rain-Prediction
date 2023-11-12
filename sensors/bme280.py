import board
from adafruit_bme280 import basic as adafruit_bme280
import math
b = 17.62
c = 243.12

def get_sensor():
    try:
        i2c = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)
    except (OSError, ValueError):
        print('BME280 not detected')
        return None

    gamma = (b * bme280.temperature /(c + bme280.temperature)) + math.log(bme280.humidity / 100.0)
    dewpoint = (c * gamma) / (b - gamma)
    bme280.dewpoint = dewpoint
    return bme280