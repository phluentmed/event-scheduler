from EventScheduler_pkg.EventScheduler import EventScheduler
import unittest
import time


def insert_into_list(item, list_object):
    list_object.append(item)


thread_name = "test_thread"


class EventSchedulerTests(unittest.TestCase):

    def test_breathing(self):
        event_scheduler = EventScheduler(thread_name)
        result = event_scheduler.start()
        self.assertEqual(result, 0)
        time.sleep(1)
        result = event_scheduler.stop()
        self.assertEqual(result, 0)

    def test_event_scheduler_stopped(self):
        event_scheduler = EventScheduler(thread_name)
        result_list = []
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        time.sleep(1)
        self.assertFalse(result_list)
        event_scheduler.start()
        event_scheduler.stop()
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        time.sleep(1)
        self.assertFalse(result_list)

    def test_no_double_start_or_stop(self):
        event_scheduler = EventScheduler(thread_name)
        event_scheduler.start()
        result = event_scheduler.start()
        self.assertEqual(result, -1)
        event_scheduler.stop()
        result = event_scheduler.stop()
        self.assertEqual(result, -1)

    def test_execute_one_event(self):
        event_scheduler = EventScheduler(thread_name)
        event_scheduler.start()
        result_list = []
        event_scheduler.enter(0, 0, insert_into_list, ('A', result_list))
        event_scheduler.stop()
        self.assertTrue(result_list)
        self.assertEqual(result_list[0], 'A')

    def test_relative_delay(self):
        event_scheduler = EventScheduler(thread_name)
        event_scheduler.start()
        result_list = []
        event_scheduler.enter(3, 0, insert_into_list, ('A', result_list))
        time.sleep(2)
        self.assertFalse(result_list)
        time.sleep(2)
        self.assertTrue(result_list)
        self.assertEqual(result_list[0], 'A')
        event_scheduler.stop()

    # TODO: Make test less flakey (failure depends on speed of execution)
    def test_priority(self):
        event_scheduler = EventScheduler(thread_name)
        event_scheduler.start()
        result_list = []
        event_scheduler.enterabs(4, 4, insert_into_list, ('C', result_list))
        event_scheduler.enterabs(4, 3, insert_into_list, ('B', result_list))
        event_scheduler.enterabs(4, 5, insert_into_list, ('D', result_list))
        event_scheduler.enterabs(4, 1, insert_into_list, ('A', result_list))
        event_scheduler.stop()
        self.assertListEqual(result_list, ['A', 'B', 'C', 'D'])
