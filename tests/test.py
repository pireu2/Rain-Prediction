import unittest
from tests.test_sensors import TestSenors
from tests.test_lcd import TestLcd


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTest(loader.loadTestsFromTestCase(TestSenors))
    suite.addTest(loader.loadTestsFromTestCase(TestLcd))

    return suite


if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
