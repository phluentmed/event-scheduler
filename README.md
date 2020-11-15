# EventScheduler Package
## Table of Contents
- [Overview](#overview)
- [Installing](#installing-dependencies)
- [Features](#features)
- [Example](#example)
- [Contact](#contact)

### Overview
Phluent's always on event scheduler is a modified version of the native python [library's scheduler](https://docs.python.org/3/library/sched.html). This means the event scheduler will always be running even with no actions. With python's sched module, a call to run() has to be made every time the number of pending events reaches zero and new events are added. With EventScheduler, only one call to start() needs to be made to start the event scheduler and it's ready to accept and run actions even when empty.

[EventScheduler GitHub](https://github.com/phluentmed/EventScheduler)

Refer to [sched.scheduler](https://github.com/python/cpython/blob/3.8/Lib/sched.py) for the descriptions of the non-modified functions.

### Installing
You should already have pip installed if you're using python > 3.4. If you don't, please visit this [link](https://pip.pypa.io/en/stable/installing/) to install it.

To install the always-on event scheduler, type the following command in the terminal.

`pip install event-scheduler`

To import the module, add the following lines in your Python file.

`from event_scheduler import EventScheduler`

To download directly visit [PyPi](https://pypi.org/project/event-scheduler/) or the [GitHub repository](https://github.com/phluentmed/PythonEventScheduler).

### Features
##### [Previous features:](https://docs.python.org/3/library/sched.html#scheduler-objects) 

`scheduler.enterabs(time, priority, action, argument=(), kwargs={})`
>
>Schedule a new event. The time argument should be a numeric type compatible with the return value of the timefunc function passed to the constructor. Events scheduled for the same time will be executed in the order of their priority. A lower number represents a higher priority.
>
>Executing the event means executing action(*argument, **kwargs). argument is a sequence holding the positional arguments for action. kwargs is a dictionary holding the keyword arguments for action.
>
>Return value is an event which may be used for later cancellation of the event (see cancel()).

`scheduler.enter(delay, priority, action, argument=(), kwargs={})`

>Delay is a relative time unit from when it enters the queue. Other than the delay parameter, this function behaves identical to enterabs().

`scheduler.cancel(event)`

> Remove the event from the queue. If event is not an event currently in the queue, this method will raise a ValueError.

`scheduler.empty()`

>Return True if the event queue is empty.

`scheduler.queue`

> Read-only attribute returning a list of upcoming events in the order they will be run. Each event is shown as a named tuple with the following fields: time, priority, action, argument, kwargs.

##### [New features:](https://github.com/phluentmed/PythonEventScheduler#readme)

`scheduler.start()` 

Triggers the EventScheduler to start running, and will start executing actions in its queue depending on delay and priority. A value of 0 is returned on a successful start up and -1 on failure to start.

`scheduler.stop()` 

Will prevent the event scheduler from taking any more actions. The event scheduler will execute the remaining actions (if any). A value of 0 is returned on a successful stop and -1 on failure to stop.

`scheduler.run(blocking=True)`

This method is now private and should not be called.
 
### Example
Please refer to this [code repository](https://github.com/phluentmed/PythonEventScheduler/tree/master/event_scheduler_example) for the example. We're going to be creating a bank account and managing transactions with an event scheduler.

In this scenario it's important to have an accurate balance. The "actions" we'll focus on are deposit and withdraw.




### Contact
Please email phluentmed@gmail.com or open an issue if you need any help using the 
code, have any questions, or even have some feature suggestions. If you're
experiencing issues, please send the corresponding stack trace or screenshot to help us diagnose the issue.

<ins>Recommended Email format: </ins>

Subject: EventScheduler - [Issue]

Steps to reproduce: (Please include code snippets or stack trace where possible)

Device used:

Platform: 

Actual result:

Expected result:

Comments:
