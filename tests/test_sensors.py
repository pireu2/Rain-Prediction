from sensors import bme280
from sensors import tsl2561
import unittest

class TestSenors(unittest.TestCase):
    def test_bme280(self):
        sensor = bme280.get_sensor()
        self.assertIsNotNone(sensor)
        self.assertGreaterEqual(sensor.temperature, -20)
        self.assertLessEqual(sensor.temperature,80)
        self.assertGreaterEqual(sensor.pressure, 300)
        self.assertLessEqual(sensor.pressure,1100)
        self.assertGreaterEqual(sensor.humidity, 0)
        self.assertLessEqual(sensor.humidity, 100)
        
    def test_tsl2561(self):
        sensor = tsl2561.get_sensor()
        self.assertIsNotNone(sensor)
        self.assertGreaterEqual(sensor.broadband, 0)
        self.assertLessEqual(sensor.broadband, 40000)

if __name__ == '__main__':
    unittest.main()