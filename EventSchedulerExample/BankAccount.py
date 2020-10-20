class BankAccount:

    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, deposit, result_handler):
        if deposit > 0:
            self.balance += deposit
            result_handler(True)
            print("You have deposited: " + str(deposit))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(False)
        print("Must deposit a positive amount \n")

    def withdraw(self, withdrawal, result_handler):
        if withdrawal <= self.balance:
            self.balance -= withdrawal
            result_handler(True)
            print("You have withdrawn: " + str(withdrawal))
            print("The new balance is: " + str(self.balance) + "\n")
            return
        result_handler(False)
        print("Insufficient funds \n")

