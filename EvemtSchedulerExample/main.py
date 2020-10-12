import BankAccount

account = BankAccount.BankAccount()
account.open_bank_account(100)
account.withdraw(50)
account.deposit(100)
account.withdraw(200)
account.deposit(50)
account.withdraw(200)
account.close_bank_account()
