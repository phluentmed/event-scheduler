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

To install the always-on event scheduler type the following command in the terminal.

`pip install Event-Scheduler-pkg-Phluent-Med==0.0.1`


To download directly you can visit this [link](https://pypi.org/project/Event-Scheduler-pkg-Phluent-Med/0.0.1/) or visit the [GitHub repository](https://github.com/phluentmed/EventScheduler).

### Features
<ins> [Previous features:](https://docs.python.org/3/library/sched.html#scheduler-objects) </ins>

`scheduler.enterabs(time, priority, action, argument=(), kwargs={})`
>
>Schedule a new event. The time argument should be a numeric type compatible with the return value of the timefunc function passed to the constructor. Events scheduled for the same time will be executed in the order of their priority. A lower number represents a higher priority.
>
>Executing the event means executing action(*argument, **kwargs). argument is a sequence holding the positional arguments for action. kwargs is a dictionary holding the keyword arguments for action.
>
>Return value is an event which may be used for later cancellation of the event (see cancel()).

`scheduler.enter(delay, priority, action, argument=(), kwargs={})`

>Schedule an event for delay more time units. Other than the relative time, the other arguments, the effect and the return value are the same as those for enterabs().

`scheduler.cancel(event)`

> Remove the event from the queue. If event is not an event currently in the queue, this method will raise a ValueError.

`scheduler.empty()`

>Return True if the event queue is empty.

`scheduler.queue`

> Read-only attribute returning a list of upcoming events in the order they will be run. Each event is shown as a named tuple with the following fields: time, priority, action, argument, kwargs.

<ins>[New features:](https://github.com/phluentmed/EventScheduler#readme)</ins>

`scheduler.start()` 

Method triggers the EventScheduler to start running, and will start executing tasks in its queue depending on delay and priority.

`scheduler.stop()` 

Method will prevent the event scheduler from taking any more tasks. If the scheduler has tasks in the queue, the scheduler goes in stopping status until it's empty then becomes stopped else it goes to stopped directly.

`scheduler.run(blocking=True)`

Is now a private method and should not be called. 
 
### Usage
In this example we're going to be creating a bank account and managing transactions with an event scheduler.

Here in this example it's important to have an accurate balance. The transactions we'll focus on are deposit and withdraw for this case.

```
class BankAccount:

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, deposit, result_handler):
        if deposit > 0:
            self.balance += deposit
            result_handler(0)  # return code of 0 indicates successful
            print("You have deposited: " + str(deposit))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(-1)  # return code of -1 indicates failure
        print("Must deposit a positive amount \n")

    def withdraw(self, withdrawal, result_handler):
        if withdrawal <= self.balance:
            self.balance -= withdrawal
            result_handler(0)  # return code of 0 indicates successful
            print("You have withdrawn: " + str(withdrawal))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(-1)  # return code of -1 indicates failure
        print("Insufficient funds \n")
```

First thing we're going to do is import the from the EventScheduler package at the top of the file.

`from EventScheduler_pkg.EventScheduler import EventScheduler`



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
