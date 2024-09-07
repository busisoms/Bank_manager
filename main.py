import re
from bank import Details, Account


def validate_password():
    password = input("Enter a password: ")
    special_symbols = ['@', '.', '#', '%']
    val = True

    if len(password) < 6 or len(password) > 13:
        print('Length should be at least 6 and be less than 13 chars')
        val = False

    if not any(char.isdigit() for char in password):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in password):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in password):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in special_symbols for char in password):
        print('Password should have at least one symbols @.#%')
        val = False
    
    if val == False:
        return validate_password()
    else:
        confirm_password = input("Confirm password: ")
        if not confirm_password == password:
            print("Passwords do not match. Please try again.")
            return validate_password()
    return password

def validate_name_and_surname():
    name = input("Enter your name: ").capitalize()
    surname = input("Enter you last name: ").capitalize()
    if not name.isalpha() or not surname.isalpha():
        print("Error: invalid name or surname")
        return validate_name_and_surname()
    return name, surname

def validate_email():
    email = input("Enter your email: ")
    if not re.match(r"[^%]+@[^#]+\.[^.]+", email):
        print("Invalid email format")
        return validate_email()
    return email

def starting_balance(new_user):
    while True:
        print("\nWould you like to enter a starting balance? \n1. Yes\n2. No")
        option = input("Enter option: ")
        if option == '1':
            starting_balance = int(input("Enter starting_balance: "))
            new_user.deposit(starting_balance)
            break
        elif option == '2':
            break
        else:
            print("Please enter one of the valid options\n")

def create_account():
        # collect user info
        user = validate_name_and_surname()
        user_name, user_surname = user
        email = validate_email()
        password = validate_password()

        # Create instances of Details and Account and save user
        details = Details(user_name, user_surname, email, password)
        details.save_to_file()
        client = Account(details)
        starting_balance(client)

        print("Account created successfully! \n")
        print(f"Welcome {user_name}, here are your details:")
        client.display_account_details()
        client.save_account()
        menu(client)

def sign_in():
    while True:
        email = input("\nEnter your email: ")
        password = input("Enter your password: ")

        # Read the details from the file
        saved_data = Details.read_from_file()
        if saved_data:
            saved_email = None
            saved_password = None
            user_found = False

            for line in saved_data.split("\n"):
                if line.startswith('Email: '):
                    saved_email = line.split(":", 1)[1].strip()
                elif line.startswith('Password: '):
                    saved_password = line.split(":", 1)[1].strip()

                if saved_email and saved_password:
                    if saved_email == email and saved_password == password:
                        user_found = True
                        break
                    else:
                        saved_email = None
                        saved_password = None

            if user_found:
                user = Account.load_account(saved_password, saved_email)
                print("Sign in successful!")
                menu(user)
                return
            else:
                print("\nNo account found with provided details. \n"
                        "Would you like to create an account? \n\n"
                        "1. Yes \n"
                        "2. No \n"
                        "3. Try again\n")

                option = input("\nEnter here: ")

                if option == '1':
                    create_account()
                elif option == '2':
                    print("Thank you for using Bank Manager")
                elif option == '3':
                    continue
                else:
                    print("Invalid option. Please enter 1 or 2")
        return


def menu(account):
    while True:
        print('\nBank Account Manager \n'
                "1. Deposit.\n"
                "2. Withdraw.\n"
                "3. Display Account details.\n"
                "4. Check Balance\n"
                "5. Exit.\n")

        option = input("Choose an option: ")
        match option:
            case "1":
                amount = int(input("Enter amount: "))
                account.deposit(amount)
            case "2":
                amount = int(input("Enter amount: "))
                account.withdraw(amount)
            case "3":
                account.display_account_details()
            case "4":
                print(account.check_balance())
            case "5":
                account.save_account()
                break
            case _:
                print("invaild option")

def start():
    print("Welcome To The Bank Account Manager.\n"
            "Do you have an account?")
    print("1.Sign in \n2.Sign up\n")

    while True:
        welcome = input("Choose an option: ")
        if welcome == "1":
            sign_in()
        elif welcome == "2":
            create_account()
        else:
            print("invalid option, Enter the given the option")

        break

if __name__ == '__main__':
    start()


