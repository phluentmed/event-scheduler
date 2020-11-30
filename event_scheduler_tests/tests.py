import unittest

unit_tests = unittest.TestLoader().discover('unit_tests', '*Tests.py')

unittest.TextTestRunner().run(unit_tests)
