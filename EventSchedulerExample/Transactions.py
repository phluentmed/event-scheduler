import BankAccount
import threading
# Importing EventScheduler package
from EventScheduler_pkg.EventScheduler import EventScheduler

# Instantiating the event scheduler with the name
scheduler = EventScheduler("transaction_threads")
# Started the scheduler so it is able to take actions
scheduler.start()
account = BankAccount.BankAccount(100)  # Initial balance of 100 dollars in the count


def is_transaction_successful(successful, location):
    if successful:
        print(location + " ATM Transaction Successful")
    else:
        print(location + " ATM Transaction Failed")


def atm_chicago_transactions(delay, priority, amount):
    if amount < 0:
        # scheduler()
        scheduler.enter(delay, priority, account.withdraw, [amount, is_transaction_successful, "Chicago"])
    else:
        scheduler.enter(delay, priority, account.deposit, [amount, is_transaction_successful, "Chicago"])


def atm_los_angeles_transactions(delay, priority, amount):
    if amount < 0:
        scheduler.enter(delay, priority, account.withdraw,
                        [amount, is_transaction_successful, "Los Angeles"])
    else:
        scheduler.enter(delay, priority, account.deposit,
                        [amount, is_transaction_successful, "Los Angeles"])


# Example 1 since Los Angeles has higher priority it will execute first
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

# Stopping the scheduler so no more actions can be done
scheduler.stop()
