import time
from sensors import bme280, tsl2561, lcd


def main():
    lcd_display = lcd.get_lcd()
    bme = bme280.get_sensor()
    tsl = tsl2561.get_sensor()
    while True:
        try:
            if lcd_display.left_button:
                lcd_display.message = f'Temperature: {bme.temperature}'
            elif lcd_display.right_button:
                lcd_display.message = f'Pressure: {bme.pressure}'
            elif lcd_display.up_button:
                lcd_display.message = f'Humidity: {bme.humidity}'
            elif lcd_display.down_button:
                lcd.message = f"Luminosity:{tsl.broadband:05}"
            elif lcd_display.select_button:
                lcd.message = f"T:{bme.temperature:.2f} P:{bme.pressure:.2f}\nH:{bme.humidity:.2f} L:{tsl.broadband:05}"
        except KeyboardInterrupt:
            print('Exit')
            break


if __name__ == '__main__':
    main()