from bank import Account
import pandas as pd

# look-up for existing clients
def sign_in():
    acc = int(input("Please enter account number to sign-in: "))
    client = Account.load(acc)
    if client:
        menu(client)
    else:
        print("Try signing-in")

# signing up new clients
def sign_up():
    name = input("Please enter you name and surname: ")
    bal = input("Starting balance, yes or no: ").lower()
    if bal == "yes":
        starting_balnce = int(input("Enter starting balance: "))
        client = Account(name, starting_balnce)
    elif bal == "no":
        client = Account(name)
    else:
        print("Please enter yes or no")
        return
    menu(client)

# Menu displayed once we are sure who is who
def menu(client):
    while True:
        print("""\n1. Deposit \n2. Withdraw \n3. Display Account Details \n4. Balance \n5. Exit \n""")
        option = input("Choose an option: ")
        match option:
            case "1":
                amount = int(input("Enter amount: "))
                client.deposit(amount)
            case "2":
                amount = int(input("Enter amount: "))
                client.withdraw(amount)
            case "3":
                client.display_acc()
            case "4":
                print(client.check_balance())
            case "5":
                client.save()
                break
            case _:
                print("invaild option")

# main program 
def start():
    print("Welcome to Bank Account Manager!\n")
    print("1. Sign-in \n2. Sign-up")
    welcome = input("Choose an option: ")
    if welcome == "1":
        sign_in()
    elif welcome == "2":
        sign_up()
    else:
        print("Please enter one of the given options")
        

# if __name__ == "__main__":
#     start()

df = pd.read_csv("accounts.csv")
print(df.to_string())