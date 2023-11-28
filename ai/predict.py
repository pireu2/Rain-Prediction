import time
import numpy as np
from sensors import bme280, tsl2561, lcd
from util.data import normalize_sensors
from ai.train import RainPrediction


def main():
    lcd_display = lcd.get_lcd()
    lcd_display.color = (255, 0, 0)
    rain_prediction = RainPrediction()
    rain_prediction.load_all_models()
    lcd_display.color = (0, 0, 255)
    while True:
        bme = bme280.get_sensor()
        # tsl = tsl2561.get_sensor()
        data = {
            "temperature": bme.temperature,
            "pressure": bme.pressure,
            "humidity": bme.humidity,
            "dewpoint": bme.dewpoint,
            "luminosity": 500,  # tsl.broadband
        }

        if lcd_display.up_button:
            lcd_display.clear()
            lcd_display.color = (255, 0, 0)
            prediction = rain_prediction.make_prediction(
                "precipitation_1h", data
            )
            lcd_display.message = f'Prediction 1h:\n{prediction}'
            time.sleep(2)
            lcd_display.color = (0, 0, 255)
        elif lcd_display.right_button:
            lcd_display.clear()
            lcd_display.color = (255, 0, 0)
            prediction = rain_prediction.make_prediction(
                "precipitation_6h", data
            )
            lcd_display.message = f'Prediction 6h:\n{prediction}'
            time.sleep(2)
            lcd_display.color = (0, 0, 255)
        elif lcd_display.down_button:
            lcd_display.clear()
            lcd_display.color = (255, 0, 0)
            prediction = rain_prediction.make_prediction(
                "precipitation_12h", data
            )
            lcd_display.message = f'Prediction 12h:\n{prediction}'
            time.sleep(2)
            lcd_display.color = (0, 0, 255)
        elif lcd_display.left_button:
            lcd_display.clear()
            lcd_display.color = (255, 0, 0)
            prediction = rain_prediction.make_prediction(
                "precipitation_24h", data
            )
            lcd_display.message = f'Prediction 24h:\n{prediction}'
            time.sleep(2)
            lcd_display.color = (0, 0, 255)
        elif lcd_display.select_button:
            lcd_display.clear()
            lcd_display.color = (0, 0, 0)
            break
        else:
            lcd_display.message = f'T:{data["temperature"]:.02f}  H:{data["humidity"]:.02f}\nP:{data["pressure"]:.02f} L:{data["luminosity"]:05f}'
            time.sleep(0.1)


if __name__ == "__main__":
    main()
