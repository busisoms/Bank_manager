import random as r
import json
import os

"""
Account class models a bank account system
using classes and objects

features:
    - check balance
    - deposit cash
    - withdrew cash
    - display_details
    - load user
    - save user
"""

class Details:
    def __init__(self, account_holder, surname, email, password, account_number=None):
        self.account_holder = account_holder
        self.surname = surname
        self.account_number = account_number if account_number is not None else 1620000 + r.randint(10000, 99999)
        self.email = email
        self.password = str(password)

    def display(self):
        print("Name:", self.account_holder)
        print("Surname:", self.surname)
        print("Email:", self.email)
        print()

    def __str__(self):
        return (
                f'Name: {self.account_holder}\n'
                f'Surname: {self.surname}\n'
                f'Account Number: {self.account_number}\n'
                f'Email: {self.email}\n'
                f'Password: {self.password}\n'
                + "_" * 30 + "\n"
                )

    def save_to_file(self, filename="details.txt"):
        try:
            with open(filename, "a") as file:
                file.write(self.__str__())
        except Exception as e:
            print(f'An error has occurred while saving file: {e}')

    @staticmethod
    def read_from_file(filename="details.txt"):
        try:
            with open(filename, "r") as file:
                contents = file.read()
                return contents
        except FileNotFoundError:
            print(f'The file {filename} does not exist.')
            return None
        except Exception as e:
            print(f'An error occurred while reading from file: {e}')
            return None

class Account:
    accounts = {
            'email': [],
            'account_holder': [],
            'account_number': [],
            'balance': []
            }

    def __init__(self, details=None, balance=0):
        if isinstance(details, Details):
            self.account_holder = details.account_holder
            self.account_number = details.account_number
            self.surname = details.surname
            self.email = details.email
        else:
            raise ValueError("The 'details' argument must be an instance of the Details class.")

        self.balance = balance


    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.")


    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")


    def display_account_details(self):
        print(f"Account Holder: {self.account_holder} {self.surname}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.balance}")
    
    def check_balance(self):
        amount = self.balance
        return f"Your current balance is: R {round(float(amount), 2)}"


    # Update only the balance if the user exists in the system
    def update(self, balance, email):
        try:
            with open('accounts.json', 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        saved_emails = data['email']
        for i in range(len(saved_emails)):
            if saved_emails[i] == email:
                data['balance'][i] = balance

        # Save to Json
        with open('accounts.json', 'w') as f:
            save = json.dumps(data)
            f.write(save)


    # add new users to json with user already
    def add(self):
        try:
            with open('accounts.json', 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        # save user's details
        data['email'].append(self.email)
        data['account_holder'].append([self.account_holder, self.surname])
        data['account_number'].append(self.account_number)
        data['balance'].append(self.balance)

        # Save new user to Json
        with open('accounts.json', 'w') as f:
            save = json.dumps(data)
            f.write(save)


    @staticmethod
    def exists(email):
        try:
            with open('accounts.json', 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            return False
        
        saved_emails = data['email']
        for i in range(len(saved_emails)):
            if saved_emails[i] == email:
                return True


    def save_account(self):
        # save user's details
        Account.accounts['email'].append(self.email)
        Account.accounts['account_holder'].append([self.account_holder, self.surname])
        Account.accounts['account_number'].append(self.account_number)
        Account.accounts['balance'].append(self.balance)

        file_exists = os.path.exists('accounts.json')

        if file_exists:
            # if the user exists in the system update balance
            if Account.exists(self.email):
                print("welcome back dude")
                self.update(self.balance, self.email)
            elif  os.stat('accounts.json').st_size > 0:
                print("def not empty")
                self.add()      
        else:
            print("can't find anyone")
            # Save new user to Json
            with open('accounts.json', 'w') as f:
                save = json.dumps(Account.accounts)
                f.write(save)
    



    # load from json
    @classmethod
    def load_account(cls, password, email):
        try:
            with open('accounts.json', 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        emails = data['email']
        for i in range(len(emails)):
            if emails[i] == email:
                name = data['account_holder'][i][0]
                surname = data['account_holder'][i][1]
                acc_number = data['account_number'][i]
                balance = data['balance'][i]

        user_details = Details(name, surname, email, password, acc_number)
        return cls(user_details, balance)




