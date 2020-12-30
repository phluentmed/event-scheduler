import unittest

unit_tests = unittest.TestLoader().discover('event_scheduler_tests/unit_tests',
                                            '*tests.py',
                                            '.')

unittest.TextTestRunner().run(unit_tests)
