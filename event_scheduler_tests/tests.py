import unittest

unit_tests = unittest.TestLoader().discover('unit_tests', '*tests.py')

unittest.TextTestRunner().run(unit_tests)
