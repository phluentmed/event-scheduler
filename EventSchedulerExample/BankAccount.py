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

