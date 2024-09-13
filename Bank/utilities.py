import sys
import time


def animate_loading(message):
    n = 10
    push_out = (len(message) + 1) * '.'
    while n > 0:
        for c in ['|', '/', '-', '\\']:
            sys.stdout.write(f'\r{message} ' + c)
            sys.stdout.flush()
            time.sleep(0.1)
        n -= 1
    sys.stdout.write(f'\r{push_out} \n')


def save_user_info(client):
    client.save_user()
    client.save_to_file()

def user_not_found(func1, func2):
    print("\nNo account found with provided details. \n"
            "Would you like to create an account? \n\n"
            "1. Yes \n"
            "2. No \n"
            "3. Try again\n")

    option = input("\nEnter here: ")

    if option == '1':
        func1()
    elif option == '2':
        print("Thank you for using Bank Manager")
    elif option == '3':
        func2()
    else:
        print("Invalid option. Please enter 1 or 2")

def menu(account):
    while True:
        print('Bank Account Manager \n'
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