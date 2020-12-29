from enum import Enum
import heapq
import sched
import sys
import threading

_sentinel = object()

# Refer to sched.scheduler for a description of non-modified functions
# https://github.com/python/cpython/blob/3.8/Lib/sched.py


class EventScheduler(sched.scheduler):
    class SchedulerStatus(Enum):
        RUNNING = 0
        STOPPING = 1
        STOPPED = 2

    def __init__(self, thread_name):
        super().__init__()
        self._scheduler_status_lock = threading.RLock()
        self._scheduler_status = self.SchedulerStatus.STOPPED
        self._event_thread = threading.Thread(target=self.run, name=thread_name)
        self._cv = threading.Condition(self._lock)
        self._timer = None

    def enterabs(self, time, priority, action, argument=(), kwargs=_sentinel):
        """Enter a new event in the queue at an absolute time.
        Returns an ID for the event which can be used to remove it,
        if necessary.
        """
        if kwargs is _sentinel:
            kwargs = {}
        with self._scheduler_status_lock:
            if self._scheduler_status != self.SchedulerStatus.RUNNING:
                # TODO: Add error message
                return None
            event = super().enterabs(time, priority, action, argument, kwargs)
            with self._cv:
                self._cv.notify()
            return event

    def enter(self, delay, priority, action, argument=(), kwargs=_sentinel):
        """A variant that specifies the time as a relative time.
        This is actually the more commonly used interface.
        """
        time = self.timefunc() + delay
        event = self.enterabs(time, priority, action, argument, kwargs)
        return event

    def cancel(self, event):
        """Remove an event from the queue.
        This must be presented the ID as returned by enter().
        If the event is not in the queue, this raises ValueError.
        """
        with self._scheduler_status_lock:
            if self._scheduler_status != self.SchedulerStatus.RUNNING:
                # TODO: Add error message
                return -1
            super().cancel(event)
            return 0

    def run(self):
        # Taken from the python library and slightly modified for an
        # always-on event scheduler. SHOULD NOT BE CALLED DIRECTLY.

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
                    timer = threading.Timer(time-now, self._notify)
                    timer.start()
                    continue

                action(*argument, **kwargs)
                delayfunc(0)  # Let other threads run

    def _notify(self):
        with self._cv:
            self._cv.notify()

    def start(self):
        with self._scheduler_status_lock:
            if self._scheduler_status != self.SchedulerStatus.STOPPED:
                # TODO: Add error message
                return -1
            self._event_thread.start()
            self._scheduler_status = self.SchedulerStatus.RUNNING
        return 0

    def stop(self):
        with self._scheduler_status_lock:
            if self._scheduler_status != self.SchedulerStatus.RUNNING:
                # TODO: Add error message
                return -1
            self._scheduler_status = self.SchedulerStatus.STOPPING
        super().enterabs(sys.maxsize, sys.maxsize, None)
        with self._cv:
            self._cv.notify()
        # TODO: Figure out the max time that we can put in here that can
        #  work for all kinds of time functions
        with self._scheduler_status_lock:
            self._event_thread.join()
            self._scheduler_status = self.SchedulerStatus.STOPPED
        return 0
