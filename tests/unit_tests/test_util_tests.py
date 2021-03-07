from event_scheduler.test_util import TestTimer
import unittest


def insert_into_list(item, list_object):
    list_object.append(item)


class TestTimerTests(unittest.TestCase):

    def tearDown(self):
        TestTimer.reset()

    def test_advance_time(self):
        self.assertEqual(TestTimer.monotonic(), 0)
        time_passed = 500
        TestTimer.advance_time(time_passed)
        self.assertEqual(TestTimer.monotonic(), time_passed)
        new_time_passed = time_passed + time_passed
        TestTimer.advance_time(time_passed)
        self.assertEqual(TestTimer.monotonic(), new_time_passed)

    def test_reset(self):
        self.assertEqual(TestTimer.monotonic(), 0)
        time_passed = 500
        TestTimer.advance_time(time_passed)
        self.assertEqual(TestTimer.monotonic(), time_passed)
        TestTimer.reset()
        self.assertEqual(TestTimer.monotonic(), 0)

    def test_timer_basic_operation(self):
        result_list = []
        item = 'A'
        time_passed = 500
        test_timer = TestTimer(time_passed,
                               insert_into_list,
                               (item, result_list))
        test_timer.start()
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(time_passed-1)
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(1)
        self.assertEqual(result_list, [item])

    def test_timer_cancel(self):
        result_list = []
        item = 'A'
        time_passed = 500
        test_timer = TestTimer(time_passed,
                               insert_into_list,
                               (item, result_list))
        test_timer.start()
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(time_passed - 1)
        self.assertListEqual(result_list, [])
        test_timer.cancel()
        TestTimer.advance_time(1)
        self.assertEqual(result_list, [])
