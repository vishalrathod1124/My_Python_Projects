import pandas as pd
import openpyxl

class ATM:
    def __init__(self, filepath="data.xlsx"):
        self.filepath = filepath
        self.current_user = None
        self.load_data()

    # Load account data from Excel
    def load_data(self):
        try:
            self.accounts = pd.read_excel(self.filepath, engine='openpyxl')
        except FileNotFoundError:
            # If the file doesn't exist, create a new one with default columns
            self.accounts = pd.DataFrame(columns=['Account Number', 'PIN', 'Balance'])
            self.save_data()

    # Save account data to Excel
    def save_data(self):
        self.accounts.to_excel(self.filepath, index=False, engine='openpyxl')

    # Function to authenticate user PIN
    def verify_pin(self, account_number, pin):
        account_row = self.accounts[self.accounts['Account Number'] == account_number]
        if not account_row.empty:
            if account_row.iloc[0]['PIN'] == pin:
                self.current_user = account_number
                print("Login successful!")
                return True
            else:
                print("Incorrect PIN. Please try again.")
        else:
            print("Account number not found.")
        return False

    # Function to check balance
    def check_balance(self):
        user_data = self.accounts[self.accounts['Account Number'] == self.current_user]
        balance = user_data.iloc[0]['Balance']
        print(f"Your current balance is: ${balance}")

    # Function to deposit money
    def deposit(self, amount):
        if amount > 0:
            self.accounts.loc[self.accounts['Account Number'] == self.current_user, 'Balance'] += amount
            self.save_data()
            print(f"${amount} deposited successfully.")
            self.check_balance()
        else:
            print("Invalid deposit amount.")

    # Function to withdraw money
    def withdraw(self, amount):
        user_data = self.accounts[self.accounts['Account Number'] == self.current_user]
        balance = user_data.iloc[0]['Balance']
        if amount > 0 and amount <= balance:
            self.accounts.loc[self.accounts['Account Number'] == self.current_user, 'Balance'] -= amount
            self.save_data()
            print(f"${amount} withdrawn successfully.")
            self.check_balance()
        elif amount > balance:
            print("Insufficient funds.")
        else:
            print("Invalid withdrawal amount.")

    # Main menu for ATM operations
    def atm_menu(self):
        while True:
            print("\nATM Menu:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit")
            choice = input("Please choose an option: ")

            if choice == '1':
                self.check_balance()
            elif choice == '2':
                try:
                    amount = float(input("Enter amount to deposit: "))
                    self.deposit(amount)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '3':
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    self.withdraw(amount)
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == '4':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    # Start the ATM interface
    def start(self):
        print("Welcome to the ATM!")
        account_number = input("Please enter your account number: ")
        pin = input("Please enter your PIN: ")

        try:
            account_number = int(account_number)
            if self.verify_pin(account_number, pin):
                self.atm_menu()
        except ValueError:
            print("Invalid account number. Please enter digits only.")

# Create ATM instance and start it
atm = ATM()
atm.start()
