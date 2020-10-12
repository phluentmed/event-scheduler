from EventScheduler_pkg.EventScheduler import EventScheduler


class BankAccount:

    def __init__(self):
        self.Event_Scheduler = EventScheduler("account_thread")
        self.Balance = 0
        self.account_open = False

    def withdraw(self, amount):
        return_code = self.Event_Scheduler.enter(0,
                                                 1,
                                                 self._withdraw,
                                                 [amount])
        if return_code == -1:
            print("Insufficient funds")
        else:
            print("You have withdrawn: " + str(amount))
            print("The new balance is: " + str(self.Balance))

    def deposit(self, amount):
        return_code = self.Event_Scheduler.enter(0,
                                                 1,
                                                 self._deposit,
                                                 [amount])
        if return_code == -1:
            print("You must deposit a positive amount")
        else:
            print("You have deposited: " + str(amount))
            print("Your new balance is: " + str(self.Balance))

    def open_bank_account(self, initial_deposit):
        self.Event_Scheduler.start()
        self.Balance = initial_deposit
        print("Bank account has been opened with: " + str(initial_deposit))

    def close_bank_account(self):
        # debating to have a while loop to check if the queue is empty to show that functionality
        self.Event_Scheduler.stop()
        print("Bank account has been closed")

    def _deposit(self, deposit):
        if deposit > 0:
            self.Balance += deposit
            return 0
        else:
            return -1

    def _withdraw(self, withdrawal):
        if withdrawal <= self.Balance:
            self.Balance -= withdrawal
            return 0
        return -1
