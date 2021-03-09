# Event Scheduler
## Table of Contents
- [Overview](#overview)
- [Installing](#installing)
- [Documentation](#documentation)
- [Quick Start](#quick-start)
- [Example](#example)
- [Contact](#contact)

### Overview
The Event Scheduler uses an internal thread to allow the application to 
schedule events to occur either ASAP or at a specified time in the future.
Instead of blocking your application's main thread, you can concurrently run
some lightweight tasks. We took some inspiration for the API design from 
[library's scheduler](https://docs.python.org/3/library/sched.html). Unlike the
native sched module, the Event Scheduler is always on and ready to accept
events. Event Scheduler is completely thread-safe too!


### Installing
You should already have pip installed if you're using python > 3.4. If you
don't, please visit this [link](https://pip.pypa.io/en/stable/installing/) to 
install it.

To install event scheduler, type the following command in the terminal:

`pip install event-scheduler`

To import the module, add the following lines in your Python file.

`from event_scheduler import EventScheduler`

To download directly visit [PyPi](https://pypi.org/project/event-scheduler/) or
the [GitHub repository](https://github.com/phluentmed/PythonEventScheduler).

## Documentation
Full documentation can be found [here](https://event-scheduler.readthedocs.io).
### Quick Start
`event_scheduler.start()`
> Enable the event scheduler to start taking events

`event_scheduler.stop(hard_stop=False)`
>Stop the event scheduler and its internal thread. Set `hard_stop` to `True`
>to stop the scheduler right away and discard all pending events. Set 
>`hard_stop` to `False` to wait for all events to finish executing at their
>scheduled times.

`event_scheduler.enter(delay, priority, action, arguments=(), kwargs={})`

>Schedule an event with a callable `action` to be executed after the `delay`.
>Events will be executed according to their `delay` and `priority` (lower 
>number = higher priority). `arguments` holds positional arguments and 
>`kwargs` hold keyword arguments for the action. Returns an event object which
>can be used to cancel the event.

`event_scheduler.cancel(event)`
>Cancel the event if it has not yet been executed.

`event_scheduler.cancel_recurring(event_id)`
>Cancel the recurring event and all future occurrences. 

```python
from event_scheduler import EventScheduler

event_scheduler = EventScheduler()
# Starts the scheduler
event_scheduler.start()
# Schedule an event that prints a message after 5 seconds
event_scheduler.enter(5, 0, print, ('5 seconds has passed since this event was entered!',))
# Schedule a recurring event that prints a message every 10 seconds
event_scheduler.enter_recurring(10, 0, print, ('10 second interval has passed!',))
```
Output:
\
`5 seconds has passed since this event was entered!`
\
`10 second interval has passed!`
\
`10 second interval has passed!`
\
`...`
 
### Example
Please refer
[here](https://pypi.org/project/event-scheduler/example/transactions.py)
for the example. 

### Contact
Please email phluentmed@gmail.com or open an issue if you need any help using
the module, have any questions, or even have some feature suggestions.

<ins>Recommended Email format: </ins>

Subject: EventScheduler - [Issue]

Steps to reproduce: (Please include code snippets or stack trace where possible)

Device used:

Platform:

Actual result:

Expected result:

Comments: