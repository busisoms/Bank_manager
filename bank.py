import random as r
import pandas as pd
import os

"""
Account class models a bank account system
using classes and objects

features:
    - check balance
    - deposit cash
    - withdrew cash
    - display_details
    - load from csv
    - save to csv
"""

class Account:
    accounts = {"acc_number":[], 
                "acc_holder":[], 
                "current_balance":[]}
    file = "accounts.csv"
    
    # Constructor
    def __init__(self, acc_holder, balance=0, acc_number=None):
        self.acc_holder = acc_holder
        self.balance = balance
        self.acc_number = acc_number if acc_number is not None else 7500000 + r.randint(10**4, 10**5 - 1)

        
    
    # Check Balance
    def check_balance(self):
        if self.balance < 0:
            self.balance = 0
        return f"Balance: R {self.balance}"
    
    # Deposit into the account
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print("Balance updated")
        else:
            print("Invalid deposit amount")

    # Withdraw from account
    def withdraw(self, amount):
        if amount <= 0:
            print(f"Can't withdraw R {amount} \nDid you mean R {abs(amount)}")
        elif amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print("Balance updated")

        
    # Display Account details
    def display_acc(self):
        print("Your details are as follows: \n")
        print(f"Account holder: {self.acc_holder}")
        print(f"Account Number: {self.acc_number}")
        print(f"Balance R {self.balance}")
        
    # save to csv
    def save(self):
        # Append the new account details to the accounts dictionary
        Account.accounts["acc_number"].append(self.acc_number)
        Account.accounts["acc_holder"].append(self.acc_holder)
        Account.accounts["current_balance"].append(self.balance)

        # Create a dataframe and save to csv
        df = pd.DataFrame(Account.accounts)
        if os.path.exists(Account.file):
            df.to_csv(Account.file, mode='a', index=False, header=False)
        else:
            df.to_csv(Account.file, index=False)

    # Statement for the user/client
    def statement(self):
        pass
    
    # load from csv
    @classmethod
    def load(cls, acc):
        df = pd.read_csv(Account.file)
        find_account = df[df["acc_number"] == acc]
        if not find_account.empty:
            acc_number = int(find_account["acc_number"].iloc[0])
            acc_holder = find_account["acc_holder"].iloc[0]
            current_balance = float(find_account["current_balance"].iloc[0])
            return cls(acc_holder, current_balance, acc_number)
        else:
            print(f"Account {acc} doesn't exist")
            return None
