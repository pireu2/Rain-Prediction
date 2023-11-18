import board
from adafruit_bme280 import basic as adafruit_bme280
import math
from constants.constants import BME280_ADDRESS, B_DEWPOINT, C_DEWPOINT


def get_sensor():
    try:
        i2c = board.I2C()
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, BME280_ADDRESS)
    except (OSError, ValueError, AttributeError):
        print("BME280 not detected")
        return None

    gamma = (
        B_DEWPOINT * bme280.temperature / (C_DEWPOINT + bme280.temperature)
    ) + math.log(bme280.humidity / 100.0)
    dewpoint = (C_DEWPOINT * gamma) / (B_DEWPOINT - gamma)
    bme280.dewpoint = dewpoint
    return bme280
