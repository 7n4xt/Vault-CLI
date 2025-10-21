import getpass

def ask_user_master_password():
    password = getpass.getpass("Enter your password: ")
    print("You entered:", password)