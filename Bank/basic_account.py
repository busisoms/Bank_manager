import json
import os
from Bank.client_details import Client
from datetime import date
from tabulate import tabulate



class Account:
    """
    A class that models a bank account system.
    
    Attribute
    ----------
    accounts: dictionary (class attribute)
        store basic user info.
    user: Client object
    balance: int

    Methods
    --------
    - 
    """
    accounts = {'email': [],
                'account_holder': [],
                'account_number': [],
                'balance': [],
                'transactions': []
                }
    account_transactions = []

    def __init__(self, user, balance=0):
        """
        Constructs all the necessary attributes for the Account object.

        Parameter
        ----------
        user: Client
            user is an instance of the class Client.
        balance: int
            the current balnce of the user.

        """
        if isinstance(user, Client):
            self.user = user
            self.account_holder = user.name + ' ' + user.surname
            self.account_number = user.account_number
            self.email = user.get_email()
        else:
            raise ValueError("The 'user' argument must be an instance of the Client class.")
        self.balance = balance


    def deposit(self, amount):
        """
        Parameter
        ---------
        amount: int
            amount to be deposited.

        Prints amount deposited and the updated balance.
        """
        if amount < 0:
            print("Can not deposit a negative value.\n")
            return False
        
        self.balance += amount
        print(f"Deposited {amount}. New balance is {self.balance}.\n")
        return True


    def withdraw(self, amount):
        """
        Parameter
        ---------
        amount: int
            amount to be withdrawn.
        
        Prints withdran amount and updated balance.
        """
        if amount < 0:
            print("Can not deposit a negative value.\n")
            return False
        
        if amount > self.balance:
            print("Insufficient balance.\n")
            return False
        
        self.balance -= amount
        print(f"Withdrew {amount}. New balance is {self.balance}.\n")
        return True


    def display_account_details(self):
        """ Prints the users details. """
        
        print("\n",str(self.user))
        print(f"Current balance is: {self.balance}\n")
    

    def check_balance(self):
        """ Returns string with user's current balance. """

        amount = self.balance
        return f"Your current balance is: R {round(float(amount), 2)}\n"
    
    def track(self, details, amount):
        d = date.today()
        if details == 'withdraw':
            amount *= -1
        transaction = [str(d), details, amount, self.balance]
        Account.account_transactions.append(transaction)
        return
    

    def transaction_history(self):
        history = Account.account_transactions
        headers = ["Date ", 'Details', 'Transaction', 'Balance']
        print(f'\n\n{tabulate(history, headers=headers)}\n')


    def update(self, balance, email):
        """
        Parameters
        -----------
        balance: int
            the user's current balance before leaving the app.
        email: str
            the user's email address.

        Updates the balance of an already existing client.
        """
        filename = '.accounts.json'
        try:
            with open(filename, 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        saved_emails = data['email']
        for i in range(len(saved_emails)):
            if saved_emails[i] == email:
                data['balance'][i] = balance

        # Save to Json
        with open(filename, 'w') as f:
            save = json.dumps(data)
            f.write(save)


    def add(self):
        """ Add new users the users file if file not empty. """
        filename = '.accounts.json'
        try:
            with open(filename, 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        # save user's details
        data['email'].append(self.email)
        data['account_holder'].append(self.account_holder)
        data['account_number'].append(self.account_number)
        data['balance'].append(self.balance)
        data['transactions'].append(Account.account_transactions)

        # Save new user to Json
        with open(filename, 'w') as f:
            save = json.dumps(data)
            f.write(save)


    @staticmethod
    def exists(email):
        """
        Parameter
        ----------

        email: str
            the user's email address.
        
        Checks whether the user is already in the system.
        """
        filename = '.accounts.json'
        try:
            with open(filename, 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            return False
        
        saved_emails = data['email']
        for i in range(len(saved_emails)):
            if saved_emails[i] == email:
                return True


    def save_account(self):
        """ Saves relevent user info to json file. """
        # save user's details
        Account.accounts['email'].append(self.email)
        Account.accounts['account_holder'].append(self.account_holder)
        Account.accounts['account_number'].append(self.account_number)
        Account.accounts['balance'].append(self.balance)
        Account.accounts['transactions'].append(Account.account_transactions)

        filename = '.accounts.json'
        file_exists = os.path.exists(filename)

        if file_exists:
            # if the user exists in the system update balance
            if Account.exists(self.email):
                self.update(self.balance, self.email)
            elif  os.stat(filename).st_size > 0:
                self.add()      
        else:
            # Save new user to Json
            with open(filename, 'w') as f:
                save = json.dumps(Account.accounts)
                f.write(save)
    

    # load from json
    @classmethod
    def load_account(cls, password, email):
        """
        Parameter
        ----------

        password: str
            the user's verifed password
        email: str
            the user's verified email address
        
        Returns an instance of Account class for an existing client
        """
        filename = '.accounts.json'
        try:
            with open(filename, 'r') as f:
                content = f.read()
                data = json.loads(content)
        except FileNotFoundError:
            print("File not found")

        emails = data['email']
        for i in range(len(emails)):
            if emails[i] == email:
                name, surname = data['account_holder'][i].split()
                acc_number = data['account_number'][i]
                balance = data['balance'][i]
                history = data['transactions'][i]

        for item in history:
            Account.account_transactions.append(item)

        user = Client(name, surname, email, password, acc_number)
        return cls(user, balance)

