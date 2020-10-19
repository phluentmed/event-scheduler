import BankAccount
from EventScheduler_pkg.EventScheduler import EventScheduler
import threading

event_scheduler = EventScheduler("transaction_threads")
event_scheduler.start()
account = BankAccount.BankAccount(100)


def atm_chicago():
    def is_transaction_successful(return_code):
        if return_code == 0:
            print("Chicago ATM Transaction Successful")
        else:
            print("Chicago ATM Transaction Failed")

    event_scheduler.enter(1, 0, account.withdraw, [90, is_transaction_successful])


def atm_los_angeles():
    def is_transaction_successful(return_code):
        if return_code == 0:
            print("Los Angeles ATM Transaction Successful")
        else:
            print("Los Angeles ATM Transaction Failed")

    event_scheduler.enter(1, 1, account.withdraw, [20, is_transaction_successful])


# Example 1
thread_atm_chicago = threading.Thread(target=atm_chicago, name="ATM Chicago")
thread_atm_los_angeles = threading.Thread(target=atm_los_angeles, name="ATM Los Angeles")
thread_atm_chicago.start()
thread_atm_los_angeles.start()
thread_atm_chicago.join()
thread_atm_los_angeles.join()

event_scheduler.stop()
