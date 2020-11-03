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
You should already have pip installed if you're using python > 3.4. If you don't please visit this [link](https://pip.pypa.io/en/stable/installing/) to install it.

To install the always-on event scheduler, type the following command in the terminal.

`pip install Event-Scheduler-pkg-Phluent-Med==0.0.1`

To download directly visit [PyPi](https://pypi.org/project/Event-Scheduler-pkg-Phluent-Med/0.0.1/) or the [GitHub repository](https://github.com/phluentmed/EventScheduler).

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

Triggers the EventScheduler to start running, and will start executing actions in its queue depending on delay and priority. A value of 0 is returned on a successful start up and -1 on failure to start.

`scheduler.stop()` 

Will prevent the event scheduler from taking any more actions. The event scheduler will execute the remaining actions (if any). A value of 0 is returned on a successful stop and -1 on failure to stop.

`scheduler.run(blocking=True)`

This method is now private and should not be called.
 
### Example
In this example, we're going to be creating a bank account and managing transactions with an event scheduler. Deposit and withdraw will be our "actions".

Here in this example it's important to have an accurate balance. The transactions we'll focus on are deposit and withdraw.

```
class BankAccount:

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, deposit, result_handler, location):
        if deposit > 0:
            self.balance += deposit
            result_handler(True, location)
            print("You have deposited: " + str(deposit))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(False, location)
        print("Must deposit a positive amount \n")

    def withdraw(self, withdrawal, result_handler, location):
        withdrawal *= -1
        if withdrawal <= self.balance:
            self.balance -= withdrawal
            result_handler(True, location)
            print("You have withdrawn: " + str(withdrawal))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(False, location)
        print("Insufficient funds \n")

```

```
import BankAccount
import threading
# Importing EventScheduler from the package
from EventScheduler_pkg.EventScheduler import EventScheduler

# Instantiating the event scheduler with the name
# EventScheduler(thread_name)
scheduler = EventScheduler("transaction_threads")

# Scheduler has been started and is able to take actions
scheduler.start()

account = BankAccount.BankAccount(100)


def is_transaction_successful(successful, location):
    if successful:
        print(location + " ATM Transaction Successful")
    else:
        print(location + " ATM Transaction Failed")


def atm_chicago_transactions(delay, priority, amount):
    if amount < 0:
        # scheduler.enter(delay, priority, argument=(), kwargs={})
        scheduler.enter(delay, priority, account.withdraw, [amount, is_transaction_successful, "Chicago"])
    else:
        # scheduler.enter(delay, priority, argument=(), kwargs={})
        scheduler.enter(delay, priority, account.deposit, [amount, is_transaction_successful, "Chicago"])


def atm_los_angeles_transactions(delay, priority, amount):
    if amount < 0:
        # scheduler.enter(delay, priority, argument=(), kwargs={})
        scheduler.enter(delay, priority, account.withdraw,
                        [amount, is_transaction_successful, "Los Angeles"])
    else:
        # scheduler.enter(delay, priority, argument=(), kwargs={})
        scheduler.enter(delay, priority, account.deposit,
                        [amount, is_transaction_successful, "Los Angeles"])


# Current balance before transactions: 100
# Example 1: Los Angeles has higher priority it will execute first
thread_atm_chicago = threading.Thread(target=atm_chicago_transactions, args=[1, 1, -90], name="ATM Chicago")
thread_atm_los_angeles = threading.Thread(target=atm_los_angeles_transactions, args=[1, 0, -20], name="ATM Los Angeles")
thread_atm_chicago.start()
thread_atm_los_angeles.start()
thread_atm_chicago.join()
thread_atm_los_angeles.join()

'''
Los Angeles ATM Transaction Successful
You have withdrawn: 20
The new balance is: 80

Chicago ATM Transaction Failed
Insufficient funds
'''

# Current balance before transactions: 80
# Example 2: Chicago's ATM will deposit first for having a lower delay and Los Angeles' ATM will be able to withdraw
# from the new balance
thread_atm_chicago = threading.Thread(target=atm_chicago_transactions, args=[3, 1, 20], name="ATM Chicago")
thread_atm_los_angeles = threading.Thread(
    target=atm_los_angeles_transactions, args=[5, 1, -100], name="ATM Los Angeles")
thread_atm_chicago.start()
thread_atm_los_angeles.start()
thread_atm_chicago.join()
thread_atm_los_angeles.join()

'''
Chicago ATM Transaction Successful
You have deposited: 20
The new balance is: 100

Los Angeles ATM Transaction Successful
You have withdrawn: 100
The new balance is: 0

Los Angeles ATM Transaction Successful
You have deposited: 60
The new balance is: 60

Chicago ATM Transaction Successful
You have withdrawn: 20
The new balance is: 40
'''

# Stopping the scheduler so no more actions can be added to the queue
scheduler.stop()
```



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
