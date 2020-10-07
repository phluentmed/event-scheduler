# EventScheduler Package
## Table of Contents
- [Overview](#overview)
- [Installing](#installing-dependencies)
- [Features](#features)
- [Usage](#usage)
- [Contact](#contact)

### Overview
Phluent's always on the Event scheduler is a modified version of the native python [library](https://docs.python.org/3/library/sched.html). The modification is for the event scheduler to always be running even with no tasks. This makes it handy for not always spinning up a new EventScheduler every time a task is received.

[EventScheduler GitHub](https://github.com/phluentmed/EventScheduler)

Refer to [sched.scheduler](https://github.com/python/cpython/blob/3.8/Lib/sched.py) for the descriptions of the non-modified functions.

### Installing
You should already have pip installed if you're using python > 3.4, in the case you don't please visit this [link](https://pip.pypa.io/en/stable/installing/) to install it.

To install the always-on event scheduler type the following command in terminal.

`pip install Event-Scheduler-pkg-Phluent-Med==0.0.1`


To download directly you can visit this [link](https://pypi.org/project/Event-Scheduler-pkg-Phluent-Med/0.0.1/) or visit the [GitHub repository](https://github.com/phluentmed/EventScheduler).

### Features
<ins>New features:</ins>

`SchedulerStatus` is an enum that has 3 statuses.

**RUNNING** : Represented by an enum value of 0, indicates the event scheduler is running and you may enter "tasks".

**STOPPING** : Represented by an enum value of 1, the event scheduler will no longer take tasks and will continue running until all tasks are completed in the queue.

**STOPPED** : Represented by an enum value of 2, is the state where the event scheduler is not running or taking any tasks.

`start` method triggers the EventScheduler to start running, and will start executing tasks in its queue.

`stop` method will prevent the event scheduler from taking any more tasks. If the scheduler has tasks in the queue, the scheduler goes in stopping status until it's empty then becomes stopped else it goes to stopped directly.

<ins>Modified features:</ins>

There is no `empty()` check for the queue anymore. If you need to access the queue to see if it's empty.

Stop the EventScheduler using `stop()`. You may have to wait for the scheduler status to change to **STOPPED**. Once stopped you can access it by `self._queue`.
 

***If you need event scheduler running and need to check if queue is empty (NOT RECOMMENDED):***

You can access it by checking if it is in an atomic state by checking `self._lock` then checking `self._queue` this is a dangerous operation and is guaranteed thus not recommended.
 

### Usage
Instantiating the event scheduler constructor, the argument it takes is the string name of the thread.

`event_scheduler = EventScheduler("new_thread_name")`


Starting the event scheduler to allow it to take tasks and start executing them.

`event_scheduler.start()`

Enqueuing task with 0 delay, 1 in priority, the task method to execute and method args.

`event_scheduler.enter(0, 1, self._method, method_args)`

Stopping the event scheduler, which will now not be allowed to enter any tasks in this state until started again.

`event_scheduler.stop()`

### Contact
Please email phluentmed@gmail.com or open an issue if you need any help using the 
code, have any questions, or even have some feature suggestions. If you're
experiencing issues, please send the corresponding stack trace or screen to help us diagnose the issue.
