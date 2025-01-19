import os
import json
import time
import admin_operations
import pwinput

USER_MENU = """
1. Sa ceara bank statement -> valoare contului
2. Sa transfere unui alt utilizator
3. Sa scoata bani din cont
4. Sa adauge bani in cont
5. Sa converteasca banii
6. Sign out
7. Exit

Type in choice: """

ADMIN_MENU = """
1. Sa se stearga clientul (admin-only)
2. Sa adauge un client nou (admin-only)
3. Sign out
4. Show users
5. Exit
"""


# ENVIRONMENT VARIABLE

# print(os.environ['admin_bank'])

def login(user: str, auth_path: str = "auth.json") -> str:
    if user == "admin":
        for _ in range(3):
            passwd = input("Type in password: ")
            if passwd == os.environ['admin_bank']:
                return user
        return ""
    else:
        with open(auth_path, "r") as f:
            credentials = json.loads(f.read())

        while user not in credentials:
            print("User not found in database.")
            user = input("Type in user: ")

        # passwd = pwinput.pwinput(prompt='PW: ', mask='*')
        passwd = input("Type in your password: ")

        while passwd != credentials[user]:
            passwd = input("Wrong password: ")

        return user


def account_balance(user: str, bank_path: str = "bank.json") -> str:
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    value = accounts[user]["value"]
    currency = accounts[user]["currency"]

    return f"Your account is worth : {value} {currency}"


def convert_account(user: str, to_currency: str, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    account = accounts[user]
    account["value"] = convert_currency(account['value'], account["currency"], to_currency)
    account["currency"] = to_currency

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    # return "Account converted from x to y"


def convert_currency(amount: int, from_currency: str, to_currency: str, currencies_json="currencies.json") -> int:
    with open(currencies_json, "r") as f:
        conversion_rates = json.loads(f.read())

    amount = amount * conversion_rates[from_currency][to_currency]

    return amount


def transfer_money(sender: str, receiver: str, amount: int, bank_path: str = "bank.json"):
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    if amount <= accounts[sender]["value"]:
        if accounts[sender]["currency"] == accounts[receiver]["currency"]:
            accounts[receiver]["value"] += amount
            accounts[sender]["value"] -= amount
        else:
            amount_receiver_currency = convert_currency(amount, accounts[sender]["currency"], accounts[receiver]["currency"])

            accounts[receiver]["value"] += amount_receiver_currency
            accounts[sender]["value"] -= amount

        with open(bank_path, "w") as f:
            f.write(json.dumps(accounts, indent=4))

        print(f"Ati transferat cu succes. Cont curent: {accounts[sender]['value']} {accounts[sender]['currency']}")

    else:
        print("Not enough money to send")


def get_username_by_phone(phone_number: str, clients_path: str = "clients.json"):
    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    for user_id, details in clients.items():
        if details['telefon'] == phone_number:
            return user_id
        print("Phone number not recognized.")
        return None



def withdraw_money(user: str, amount: int, bank_path: str = "bank.json"):
    """Allow user to withdraw money from their account."""
    try:
        file = open(bank_path, "r")
        accounts = json.load(file)
        file.close()

        if user in accounts:
            if accounts[user]["value"] >= amount:
                accounts[user]["value"] -= amount
                file = open(bank_path, "w")
                json.dump(accounts, file, indent=4)
                file.close()
                print(f"Successfully withdrew {amount} {accounts[user]['currency']}. New balance: {accounts[user]['value']} {accounts[user]['currency']}.")
            else:
                print("Insufficient funds.")
        else:
            print("User account not found.")
    except FileNotFoundError:
        print("Error: Bank data not found.")



def deposit_money(user: str, amount: int, bank_path: str = "bank.json"):
    """Allow user to deposit money into their account."""
    try:
        file = open(bank_path, "r")
        accounts = json.load(file)
        file.close()

        if user in accounts:
            accounts[user]["value"] += amount
            file = open(bank_path, "w")
            json.dump(accounts, file, indent=4)
            file.close()
            print(f"Successfully added {amount} {accounts[user]['currency']}. New balance: {accounts[user]['value']} {accounts[user]['currency']}.")
        else:
            print("User account not found.")
    except FileNotFoundError:
        print("Error: Bank data not found.")



def add_new_client(username: str, password: str, initial_balance: int, currency: str, auth_path: str = "auth.json", bank_path: str = "bank.json"):
    """Admin function to add a new client."""
    try:
        file = open(auth_path, "r")
        credentials = json.load(file)
        file.close()
    except FileNotFoundError:
        credentials = {}

    try:
        file = open(bank_path, "r")
        accounts = json.load(file)
        file.close()
    except FileNotFoundError:
        accounts = {}

    if username in credentials:
        print("User already exists. Choose a different username.")
        return

    credentials[username] = password
    file = open(auth_path, "w")
    json.dump(credentials, file, indent=4)
    file.close()

    accounts[username] = {"value": initial_balance, "currency": currency}
    file = open(bank_path, "w")
    json.dump(accounts, file, indent=4)
    file.close()

    print(f"Successfully added new user: {username} with balance: {initial_balance} {currency}.")



if __name__ == '__main__':
    username = input("Please enter your username: ")
    username = login(username)
    menu = USER_MENU if username != "admin" else ADMIN_MENU

    user_pick = input(menu)

    while True:
        if username != "admin":
            match user_pick:
                case "1":
                    print(account_balance(username))
                case "2":
                    amount = int(input("Citeste de la tastatura suma de bani in valuta personala: "))
                    phone_number = input("Cui vrei sa ii trimiti bani? Introdu nr de tel: ")
                    receiver_id = get_username_by_phone(phone_number)
                    if receiver_id:
                        transfer_money(username, receiver_id, amount)

                case "3":
                    amount = int(input("Enter the amount to withdraw: "))
                    withdraw_money(username, amount)
                case "4":
                    amount = int(input("Enter the amount to deposit: "))
                    deposit_money(username, amount)
                case "5":
                    currency = input("Ce vrei sa transformi? ")
                    # verificati sa fie currency corect
                    convert_account(username, currency)
                case "6":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "7":
                    exit(0)
                case "8":
                    pass
                case _:
                    pass
            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)
        else:
            match user_pick:
                case "1":
                    user_to_delete = input("Ce user doresti sa stergi? ")
                    admin_operations.remove_user(user_to_delete)

                case "2":
                    new_user = input("Enter the username for the new client: ")
                    new_password = input("Enter the password for the new client: ")
                    initial_balance = int(input("Enter the initial balance for the new client: "))
                    currency = input("Enter the currency for the new client: ")
                    add_new_client(new_user, new_password, initial_balance, currency)
                case "3":
                    username = input("Citeste un nou user: ")
                    username = login(username)
                case "4":
                    with open("bank.json", "r") as f:
                        print(f.read())
                case "5":
                    # option 1
                    # break
                    exit(0)

            time.sleep(3)
            menu = USER_MENU if username != "admin" else ADMIN_MENU
            user_pick = input(menu)
