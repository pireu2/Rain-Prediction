import lcd
import unittest

class TestLcd(unittest.TestCase):
    def test_lcd(self):
        lcd_screen = lcd.get_lcd()
        self.assertIsNotNone(lcd_screen)

if __name__ == '__main__':
    unittest.main()