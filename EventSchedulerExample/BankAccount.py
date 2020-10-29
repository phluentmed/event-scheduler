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

