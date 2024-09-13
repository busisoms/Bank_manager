from Bank.basic_account import Account
from Bank.client_details import Client
from Bank.verification import *
from Bank.utilities import *


def create_account():
    # collect user info
    user = validate_name_and_surname()
    user_name, user_surname = user
    email = validate_email()

    while True:
        password = validate_password()
        confirm_pass = verify_password(password)
        if confirm_pass:
            animate_loading('Confirming password.......')
            # Create instances of Details and Account and save user
            client = Client(user_name, user_surname, email, password)
            save_user_info(client)
            user_account = Account(client)
            starting_balance(user_account)
            animate_loading('Almost there......')
            print(f"\nAccount created successfully!\nWelcome {user_name} \n")
            break
        else: print("Password doesn't match")  
    menu(user_account)
    return

def starting_balance(user):
    while True:
        print("\nYou need a minimum starting balance of R20 or greater to start.\n")
        amount = float(input("Enter Starting amount: R"))
        if amount <= 19:
            print("Deposit amount has to be above R10.")
        else:
            user.deposit(amount)
            return

def sign_in():
    email = validate_email()
    password = validate_password()
    animate_loading('signing in......')

    user = Client.find_user(email)
    if user is not None:
        key = user[email][1][0]
        saved_password = user[email][1][1]
        confirm_password = Client.verify_pass(password, key)

        if saved_password == confirm_password:
            user_account = Account.load_account(saved_password, email)
            print("Sign in successful!")
            menu(user_account)
            return
        else:
            animate_loading('Loading........')
            user_not_found(create_account, sign_in)

    user_not_found(create_account, sign_in)
    return