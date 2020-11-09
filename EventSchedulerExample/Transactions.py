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


def atm_chicago_transactions(transactions):
    for transaction in transactions:
        delay, priority, amount = transaction
        if amount < 0:
            # scheduler.enter(delay, priority, argument=(), kwargs={})
            scheduler.enter(delay, priority, account.withdraw, [amount, is_transaction_successful, "Chicago"])
        else:
            # scheduler.enter(delay, priority, argument=(), kwargs={})
            scheduler.enter(delay, priority, account.deposit, [amount, is_transaction_successful, "Chicago"])


def atm_los_angeles_transactions(transactions):
    for transaction in transactions:
        delay, priority, amount = transaction
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
thread_atm_chicago = threading.Thread(target=atm_chicago_transactions, args=[[(1, 1, -90)]], name="ATM Chicago")
thread_atm_los_angeles = threading.Thread(
    target=atm_los_angeles_transactions, args=[[(1, 0, -20)]], name="ATM Los Angeles")
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
# from the new balance. Los Angeles ATM will be able to deposit before Chicago's ATM withdraws due to higher priority
# thus making both transactions successful.
thread_atm_chicago = threading.Thread(
    target=atm_chicago_transactions, args=[[(3, 1, 20), (5, 2, -20)]], name="ATM Chicago")
thread_atm_los_angeles = threading.Thread(
    target=atm_los_angeles_transactions, args=[[(4, 1, -100), (5, 1, 60)]], name="ATM Los Angeles")

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
