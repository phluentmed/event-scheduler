from enum import Enum
import heapq
from sched import Event
import sched
import sys
from time import monotonic
from time import sleep
import threading

_sentinel = object()

# Refer to sched.scheduler for a description of non-modified functions
# https://github.com/python/cpython/blob/3.8/Lib/sched.py


class SchedulerStatus(Enum):
    RUNNING = 0
    STOPPING = 1
    STOPPED = 2


class EventScheduler():

    def __init__(self,
                 thread_name=None,
                 timefunc=monotonic,
                 delayfunc=sleep):
        self._queue = []
        self._lock = threading.RLock()
        self.timefunc = timefunc
        self.delayfunc = delayfunc
        self._scheduler_status = SchedulerStatus.STOPPED
        self._event_thread = threading.Thread(target=self.run,
                                              name=thread_name)
        # Condition variable to notify the event thread when there's a new
        # event or when the deadline of the soonest event has passed.
        self._cv = threading.Condition(self._lock)
        # If we've looked at the front of the queue and the event isn't ready
        # to execute, we set a timer for the remaining time. If a new event is
        # added to the queue, then we cancel the timer and set it to None.
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
        If the event is not in the queue, this raises ValueError.
        """
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return -1
            self._queue.remove(event)
            heapq.heapify(self._queue)
            self._notify()

    def run(self):
        # SHOULD NOT BE CALLED DIRECTLY.

        """Execute events until the queue is empty.
        If blocking is False executes the scheduled events due to
        expire soonest (if any) and then return the deadline of the
        next scheduled call in the scheduler.
        When there is a positive delay until the first event, the
        delay function is called and the event is left in the queue;
        otherwise, the event is removed from the queue and executed
        (its action function is called, passing it the argument).  If
        the delay function returns prematurely, it is simply
        r.RUNNING.
        It is legal for both the delay function and the action
        function to modify the queue or to raise an exception;
        exceptions are not caught but the scheduler's state remains
        well-defined so run() may be called again.
        A questionable hack is added to allow other threads to run:
        just after an event is executed, a delay of 0 is executed, to
        avoid monopolizing the CPU when other threads are also
        runnable.
        """
        # localize variable access to minimize overhead
        # and to improve thread safety
        cv = self._cv
        q = self._queue
        timer = self._timer
        delayfunc = self.delayfunc
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
                    timer = threading.Timer(time-now, self._notify)
                    timer.start()
                    continue

                action(*argument, **kwargs)
                delayfunc(0)  # Let other threads run

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

    def stop(self):
        # TODO: Figure out the max time that we can put in here that can
        #  work for all kinds of time functions
        event = Event(sys.maxsize, sys.maxsize, None, (), {})
        with self._lock:
            if self._scheduler_status != SchedulerStatus.RUNNING:
                return -1
            self._scheduler_status = SchedulerStatus.STOPPING
            heapq.heappush(self._queue, event)
            self._notify()
        self.delayfunc(0) # let other threads fun since the next line is a join
        self._event_thread.join()
        with self._lock:
            self._scheduler_status = SchedulerStatus.STOPPED
        return 0
