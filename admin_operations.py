import json


def remove_user(user_to_be_deleted: str, bank_path: str = "bank.json", auth_path: str = "auth.json" , clients_path: str = "clients.json"):
# here i need to change the program to make it more efficient
# heyyya Zsuzsa
# kajsdnasjkdnjksndkajsdnkjsdnk
# ne legyel ideges
    with open(bank_path, "r") as f:
        accounts = json.loads(f.read())

    with open(auth_path, "r") as f:
        credentials = json.loads(f.read())

    with open(clients_path, "r") as f:
        clients = json.loads(f.read())

    accounts.pop(user_to_be_deleted, None)
    credentials.pop(user_to_be_deleted, None)
    clients.pop(user_to_be_deleted, None)

    with open(bank_path, "w") as f:
        f.write(json.dumps(accounts, indent=4))

    with open(auth_path, "w") as f:
        f.write(json.dumps(credentials, indent=4))

    with open(clients_path, "w") as f:
        f.write(json.dumps(clients, indent=4))


def add_user():
    pass