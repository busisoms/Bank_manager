import re

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
    return password


def verify_password(password):
    confirm_password = input("Confirm password: ")
    if not confirm_password == password:
        print("Passwords do not match. Please try again.")
        return False
    return True
    

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