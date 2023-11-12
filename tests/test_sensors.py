import sensors.bme280
import sensors.tsl2561
import unittest

class TestSenors(unittest.TestCase):
    def test_bme280(self):
        sensor = sensors.bme280.get_sensor()
        self.assertNotNone(sensor)
        self.assert