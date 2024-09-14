from Bank.auth_system import sign_in, create_account


print("Welcome To The Bank Account Manager.\n")
print("1.Sign in \n2.Sign up\n")

while True:
    welcome = input("Choose an option: ")
    if welcome == "1":
        sign_in()
        break
    elif welcome == "2":
        create_account()
        break
    else:
        print("invalid option, Enter the given the option")



