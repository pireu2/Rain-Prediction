import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd


def get_lcd():
    lcd_columns = 16
    lcd_rows = 2

    try:
        i2c = board.I2C()
        lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)
    except (OSError, ValueError):
        print("LCD not detected")
        return None
    lcd.color = [0, 0, 0]
    lcd.clear()

    return lcd
