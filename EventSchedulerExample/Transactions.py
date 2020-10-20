import BankAccount
# Importing EventScheduler package
from EventScheduler_pkg.EventScheduler import EventScheduler

# Instantiating the event scheduler with the name
scheduler = EventScheduler("transaction_threads")
# Started the scheduler so it is able to take actions
scheduler.start()
account = BankAccount.BankAccount(100)  # Initial balance of 100 dollars in the count


def atm_chicago():
    def is_transaction_successful(successful):
        if successful:
            print("Chicago ATM Transaction Successful")
        else:
            print("Chicago ATM Transaction Failed")

    scheduler.enter(1, 1, account.withdraw, [90, is_transaction_successful])  # note priority is at 1


def atm_los_angeles():
    def is_transaction_successful(successful):
        if successful:
            print("Los Angeles ATM Transaction Successful")
        else:
            print("Los Angeles ATM Transaction Failed")

    scheduler.enter(1, 0, account.withdraw, [20, is_transaction_successful])  # note priority here is 0


# Example 1 since Los Angeles has higher priority it will execute first
atm_chicago()
atm_los_angeles()

'''
Los Angeles ATM Transaction Successful
You have withdrawn: 20
The new balance is: 80

Chicago ATM Transaction Failed
Insufficient funds
'''

# Stopping the scheduler so no more actions can be done
scheduler.stop()
