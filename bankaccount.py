class BankAccount:
    def __init__(self, account_holder, intial_balance=0):
        """
        Constructor to initialize a new bank account

        : param account_holder: Name of the account holder
        : param initial_balance: The initial balance for the account (default is 0)
        """

        self.account_holder = account_holder  # Name of the account holder
        self.balance = intial_balance  # Starting balance of the account

        # Print a message when a new account is created
        print(f"Account acreated for {self.account_holder} with balance {self.balance}")

    def deposit(self, amount):
        """
        Deposit money into the account.

        :param amount: The amount to deposit into the account
        """
        try:
            if amount <= 0:
                raise ValueError("deposit amount must be positive")
            self.balance += amount
            print(f"Deposited {amount}. New balance is {self.balance}")
        except ValueError as e:
            print(f"Error: {e}")

    def withdraw(self, amount):
        """
        Withdraw money from the account.

        :param amount: The amount to withdraw from the account.
        """
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
            elif amount > self.balance:
                raise ValueError("Insufficient funds")
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}")
        except ValueError as e:
            print(f"Error: {e}")

    def get_balance(self):
        """
        Get the current balance of the account.
        """
        return self.balance

    def __str__(self):
        """
        Return a string representation of the BankAccount object.
        This will be used when printing an instance of BankAccount.
        """
        return f"Account holder: {self.account_holder}, Balance: ${self.balance}"


# Create a bank account object for Alice
alice_account = BankAccount("Alice", 1000)

# Performing some operations
alice_account.deposit(500)
alice_account.withdraw(300)
alice_account.withdraw(1500)  # Insufficient funds

# Checking the final balance
print(f"Final balance: {alice_account.get_balance()}")

# Print the string representation of the account
print(alice_account)
