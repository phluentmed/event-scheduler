import threading
from event_scheduler import EventScheduler


class TestTimer(threading.Timer):
    """The TestTimer is designed to test your code that incorporates the event
    scheduler. Passing the TestTimer.monotonic and TestTimer into the event
    scheduler gives you full control of the event scheduler's monotonic time.
    Passing the event scheduler's condition variable enables full
    synchronization with the event scheduler's internal thread.
    """
    _time = 0
    _observers = []
    _event_scheduler = None
    _cv = None

    @classmethod
    def monotonic(cls) -> float:
        if not cls._cv:
            return cls._time
        with cls._cv:
            return cls._time

    @classmethod
    def advance_time(cls, increment: float) -> None:
        if increment < 0:
            raise ValueError('Time increment must be positive.')
        if not cls._cv:
            cls._time += increment
            for observer in cls._observers:
                observer.run()
            return
        with cls._cv:
            cls._time += increment
            # synchronize with the event scheduler thread (only advance time
            # when the thread isn't active.
            cls._cv.wait_for(lambda: len(cls._cv._waiters) != 0, 1)
            did_run = False
            for observer in cls._observers:
                result = observer.run()
                did_run = did_run or result
            # if we executed the function for the timer (in this case a notify
            # on the condition variable, we have to wait until the event
            # scheduler has done work (we get notified in that case).
            if did_run:
                cls._cv.wait()

    # pass in the event scheduler's condition variable for synchronization.
    @classmethod
    def set_event_scheduler(cls, event_scheduler: EventScheduler):
        cls._event_scheduler = event_scheduler
        cls._cv = event_scheduler._cv

    @classmethod
    def reset(cls):
        cls._time = 0
        cls._observers = []
        cls._event_scheduler = None
        cls._cv = None

    def __init__(self, interval, function, args=None, kwargs=None):
        threading.Thread.__init__(self)
        self.done_time = TestTimer.monotonic() + interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}

    def start(self):
        TestTimer._observers.append(self)

    def cancel(self):
        """Stop the timer if it hasn't finished yet."""
        if self in TestTimer._observers:
            TestTimer._observers.remove(self)

    def run(self):
        if self.done_time <= TestTimer.monotonic():
            self.function(*self.args, **self.kwargs)
            TestTimer._observers.remove(self)
            return True
        return False
