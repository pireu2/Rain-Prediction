import time
from sensors import bme280, tsl2561, lcd
from util.data import normalize_sensors


def main():
    lcd_display = lcd.get_lcd()

    while True:
        bme = bme280.get_sensor()
        tsl = tsl2561.get_sensor()
        data = {
            'temperature': bme.temperature,
            'pressure': bme.pressure,
            'humidity': bme.humidity,
            'dewpoint': bme.dewpoint,
            'luminosity': tsl.broadband
        }
        normalize_sensors(data)
        try:
            if lcd_display.left_button:
                lcd_display.message = f'Temp: {data["temperature"]}'
            elif lcd_display.right_button:
                lcd_display.message = f'Pressure: {data["pressure"]}'
            elif lcd_display.up_button:
                lcd_display.message = f'Humidity: {data["humidity"]}'
            elif lcd_display.down_button:
                lcd_display.message = f"Luminosity:{data['luminosity']}"
            elif lcd_display.select_button:
                lcd_display.message = f"T:{data['temperature']:.2f} P:{data['pressure']:.2f}\nH:{data['humidity']:.2f} L:{data['luminosity']:06}"
                # lcd_display.message = f"Dewpoint: {bme.dewpoint}"
            else:
                time.sleep(0.1)
                lcd_display.clear()
        except KeyboardInterrupt:
            print('Exit')
            break


if __name__ == '__main__':
    main()