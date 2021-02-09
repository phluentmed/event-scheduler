from event_scheduler.event_scheduler import EventScheduler
from event_scheduler.test_util import TestTimer
import unittest
import time


def insert_into_list(item, list_object: list):
    list_object.append(item)


TEST_THREAD = "test_thread"


class EventSchedulerTests(unittest.TestCase):

    def tearDown(self) -> None:
        TestTimer.reset()

    def test_breathing(self):
        event_scheduler = EventScheduler(TEST_THREAD)
        result = event_scheduler.start()
        self.assertEqual(result, 0)
        result = event_scheduler.stop()
        self.assertEqual(result, 0)

    def test_event_scheduler_stopped(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        result_list = []
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        TestTimer.advance_time(0)
        self.assertFalse(result_list)
        event_scheduler.start()
        event_scheduler.stop()
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        TestTimer.advance_time(0)
        self.assertFalse(result_list)

    def test_no_double_start_or_stop(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        event_scheduler.start()
        result = event_scheduler.start()
        self.assertEqual(result, -1)
        event_scheduler.stop()
        result = event_scheduler.stop()
        self.assertEqual(result, -1)

    def test_execute_one_event(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        event_scheduler.start()
        result_list = []
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        event_scheduler.stop()
        self.assertTrue(result_list)
        self.assertEqual(result_list[0], 'A')

    def test_relative_delay(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        item = 'A'
        event_scheduler.enter(3, 0, insert_into_list, (item, result_list))
        TestTimer.advance_time(2)
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(1)
        self.assertListEqual(result_list, [item])
        event_scheduler.stop()

    def test_priority(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(4, 4, insert_into_list, ('C', result_list))
        event_scheduler.enterabs(4, 3, insert_into_list, ('B', result_list))
        event_scheduler.enterabs(4, 5, insert_into_list, ('D', result_list))
        event_scheduler.enterabs(4, 1, insert_into_list, ('A', result_list))
        TestTimer.advance_time(3.8)
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(0.3)
        event_scheduler.stop()
        self.assertListEqual(result_list, ['A', 'B', 'C', 'D'])

    def test_multiple_events_different_times(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(5, 1, insert_into_list, ('D', result_list))
        event_scheduler.enterabs(4, 1, insert_into_list, ('B', result_list))
        event_scheduler.enterabs(7, 1, insert_into_list, ('E', result_list))
        event_scheduler.enterabs(1, 1, insert_into_list, ('A', result_list))
        self.assertListEqual(result_list, [])
        TestTimer.advance_time(1)
        self.assertListEqual(result_list, ['A'])
        TestTimer.advance_time(3)
        self.assertListEqual(result_list, ['A', 'B'])
        event_scheduler.enterabs(0.5, 1, insert_into_list, ('C', result_list))
        TestTimer.advance_time(1)
        self.assertListEqual(result_list, ['A', 'B', 'C', 'D'])
        TestTimer.advance_time(2)
        self.assertListEqual(result_list, ['A', 'B', 'C', 'D', 'E'])
        event_scheduler.stop()

    def test_event_time_in_the_past(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(-1, 1, insert_into_list, ('A', result_list))
        TestTimer.advance_time(0)
        event_scheduler.stop()
        self.assertListEqual(result_list, ['A'])

    def test_cancel_event(self):
        event_scheduler = EventScheduler(TEST_THREAD,
                                         TestTimer.monotonic,
                                         TestTimer)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        event = event_scheduler.enterabs(2,
                                         1,
                                         insert_into_list,
                                         ('A', result_list))
        event_scheduler.enterabs(2, 3, insert_into_list, ('B', result_list))
        TestTimer.advance_time(1)
        event_scheduler.cancel(event)
        TestTimer.advance_time(1)
        event_scheduler.stop()
        self.assertListEqual(result_list, ['B'])

    def test_multiple_events_built_in_timer(self):
        # We should test the built-in timer to make sure it's working as
        # expected. We can also test the hard stop being set to false, (the
        # event scheduler should execute all remaining events in the queue
        # before stopping).
        event_scheduler = EventScheduler(TEST_THREAD)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(0.2, 1, insert_into_list, ('A', result_list))
        event_scheduler.enterabs(0.4, 1, insert_into_list, ('B', result_list))
        event_scheduler.enterabs(0.7, 1, insert_into_list, ('C', result_list))
        event_scheduler.enterabs(1, 1, insert_into_list, ('D', result_list))
        event_scheduler.stop(False)
        self.assertListEqual(result_list, ['A', 'B', 'C', 'D'])

    def test_stop_scheduler_hard_stop(self):
        # With a hard stop, the event scheduler clear all of the upcoming
        # events from the queue when stopping.
        event_scheduler = EventScheduler(TEST_THREAD)
        TestTimer.set_event_scheduler(event_scheduler)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(30, 1, insert_into_list, ('A', result_list))
        event_scheduler.stop(True)
        self.assertListEqual(result_list, [])
