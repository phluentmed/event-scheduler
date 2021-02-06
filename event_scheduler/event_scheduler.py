from enum import Enum
import heapq
from sched import Event
import sys
from time import monotonic
from time import sleep
import threading

_sentinel = object()

# Designed using elements from sched.scheduler from
# https://github.com/python/cpython/blob/3.8/Lib/sched.py


class SchedulerStatus(Enum):
    RUNNING = 0
    STOPPING = 1
    STOPPED = 2


class EventScheduler:

    def __init__(self,
                 thread_name=None,
                 timefunc=monotonic,
                 timer_class=threading.Timer):
        self._queue = []
        self._lock = threading.RLock()
        self.timefunc = timefunc
        self._scheduler_status = SchedulerStatus.STOPPED
        self._event_thread = threading.Thread(target=self._run,
                                              name=thread_name)
        # Condition variable to notify the event thread when there's a new
        # event or when the deadline of the soonest event has passed.
        self._cv = threading.Condition(self._lock)
        # If we've looked at the front of the queue and the event isn't ready
        # to execute, we set a timer for the remaining time. If a new event is
        # added to the queue, then we cancel the timer and set it to None.
        self._timer_class = timer_class
        self._timer = None

    def _notify(self):
        with self._cv:
            self._cv.notify()

    def enterabs(self, time, priority, action, argument=(), kwargs=_sentinel):
        """Enter a new event in the queue at an absolute time.
        Returns an ID for the event which can be used to remove it,
        if necessary.
        """
        if kwargs is _sentinel:
            kwargs = {}
        event = Event(time, priority, action, argument, kwargs)
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return None
            heapq.heappush(self._queue, event)
            self._notify()
        return event # The ID

    def enter(self, delay, priority, action, argument=(), kwargs=_sentinel):
        """A variant that specifies the time as a relative time.
        This is actually the more commonly used interface.
        """
        time = self.timefunc() + delay
        return self.enterabs(time, priority, action, argument, kwargs)

    def cancel(self, event):
        """Remove an event from the queue.
        This must be presented the ID as returned by enter().
        If the event is not in the queue, this is a no-op.
        """
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return -1
            try:
                self._queue.remove(event)
                heapq.heapify(self._queue)
                self._notify()
            except ValueError:
                pass
        return 0

    def cancel_all(self):
        """Clear all events from the queue.
        If the queue is already empty, this is a no-op.
        """
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return -1
            if self._queue:
                self._queue.clear()
                self._notify()
        return 0

    def _run(self):
        """ Execute events with the soonest time and lowest priority events
        executing first. If there aren't any events available to run, this
        thread uses a timer and waits on a condition variable. When the
        deadline for the event has passed, the timer calls notify() on the
        condition variable and the event action is executed.

        A terminating event is enqueued when the event scheduler is stopped
        and joins the event scheduler thread once the queue is drained.
        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        cv = self._cv
        q = self._queue
        timer = self._timer
        timefunc = self.timefunc
        pop = heapq.heappop
        while True:
            with cv:
                if not q or timer:
                    cv.wait()
                if timer:
                    timer.cancel()
                    timer = None
                time, priority, action, argument, kwargs = q[0]
                if priority == sys.maxsize:
                    pop(q)
                    self._notify()
                    break
                now = timefunc()
                if time > now:
                    delay = True
                else:
                    delay = False
                    pop(q)
                if delay:
                    # Initialize a timer to wake up this thread when the first
                    # event is ready to execute.
                    timer = self._timer_class(time-now, self._notify)
                    timer.start()
                    self._notify()
                    continue

                action(*argument, **kwargs)
                self._notify()

    @property
    def queue(self):
        """An ordered list of upcoming events.
                Events are named tuples with fields for:
                    time, priority, action, arguments, kwargs
                """
        # Use heapq to sort the queue rather than using 'sorted(self._queue)'.
        # With heapq, two events scheduled at the same time will show in
        # the actual order they would be retrieved.
        with self._lock:
            events = self._queue[:]
            self._notify()
        return list(map(heapq.heappop, [events] * len(events)))

    def start(self):
        with self._lock:
            if self._scheduler_status != SchedulerStatus.STOPPED:
                return -1
            self._event_thread.start()
            self._scheduler_status = SchedulerStatus.RUNNING
        return 0

    def stop(self, hard_stop: bool = False):
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return -1
            if hard_stop:
                self.cancel_all()
            self._scheduler_status = SchedulerStatus.STOPPING
            last_event = Event(self.timefunc(), 0, None, (), {})
            if self._queue:
                last_event = max(self._queue)
            # we want to make sure the "terminating" event is the last one in
            # the queue
            event = Event(last_event.time,
                          sys.maxsize,
                          None,
                          (),
                          {})
            heapq.heappush(self._queue, event)
            self._notify()
        sleep(0)  # let other threads run since the next line is a join
        self._event_thread.join()
        with self._lock:
            self._scheduler_status = SchedulerStatus.STOPPED
        return 0
