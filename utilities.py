"""This module contains useful functions used in the program."""
import json
import pandas
import datetime as dt
import csv
import os.path
from member_factory import Customer, Official


def start():
    transaction = input(
        "\nWhat would you like to do?\n\n"
        "1. Open an account.\n"
        "2. Do giveaway a.k.a. Transfer money.\n"
        "3. Deposit money.\n"
        "4. Withdraw money.\n"
        "5. Check balance.\n"
        "6. Account statement.\n"
        "7. Change password.\n"
        "8. Admin transactions.\n\n"
        "Reply with a number to begin transaction: "
    )

    match transaction:
        case "1":
            open_account()
        case "2":
            transfer()
        case "3":
            deposit()
        case "4":
            withdraw()
        case "5":
            check_balance()
        case "6":
            get_account_statement()
        case "7":
            change_password()
        case "8":
            admin_start()
        case default:
            print("\n\nSorry, invalid input!!🤬😡")
            again()


def login():
    print("\nPlease login to authorize transaction.")
    email = input("\nYour email: ")
    password = input("Your password: ")

    if not email or not password:
        print("\nSorry, invalid input!🤬😡")
        return None
    try:
        database = pandas.read_json("database.json")
    except ValueError:
        print("\nSorry, email and password not found. No database!😓")
        return None
    else:
        if email in database:
            if database[email]["password"] == password:
                print("\nLogin Successful!🙂")
                if database[email]["role"] == "customer":
                    return Customer(
                        database[email]["name"],
                        email,
                        database[email]["password"], database[email]["account type"],
                        database[email]["balance"]
                    )
                else:
                    return Official(database[email]["name"], database[email]["email"], database[email]["password"])
            else:
                print("\nSorry, password incorrect!!😓")
                return None
        else:
            print("\nSorry, email not found!!😪")
            return None


def record(user_email, transaction, amount, name=None):
    now = dt.datetime.now()
    data = {
        "user": user_email,
        "time": f"{now.hour}:{now.minute}",
        "date": f"{now.date()}",
        "transaction": transaction,
        "amount": amount,
        "account": name
    }
    fields = ["user", "time", "date", "transaction", "amount", "account"]
    if os.path.exists("./records.csv"):
        with open("records.csv", "a", newline="") as file:
            output_writer = csv.DictWriter(file, fieldnames=fields)
            output_writer.writerow(data)
    else:
        with open("records.csv", "w", newline="") as file:
            output_writer = csv.DictWriter(file, fieldnames=fields)
            output_writer.writeheader()
            output_writer.writerow(data)
    return data


def open_account():
    print("Opening account...")
    name = input("What is the name for the account? ").title()
    email = input("What is the email for the account? ")
    account_type = input(
        "What type of account would you like to create?\n"
        "Type 'S' for a savings account or 'C' for a current account: "
    ).lower()
    password1 = input("Type a password to secure your account: ")
    password2 = input("Please confirm password: ")

    if not name or not email or not password1 or not password2 or account_type not in ["s", "c"]:
        print("\nSorry, invalid inputs!! Make sure to fill all fields correctly!!🤬😡")
        again()
        return

    if password1 != password2:
        print("\nSorry, passwords do not match!!😡")
        again()
        return
    try:
        database = pandas.read_json("database.json")
    except ValueError:
        pass
    else:
        if email in database.columns:
            print("\nSorry, this email already exists in our database. Please use another email.🙁")
            again()
            return
    account_type = "savings" if account_type == "s" else "current"
    new_customer = Customer(name, email, password1, account_type)

    print(f"\nSuccess!! Account has been created. The account number is: {new_customer.account_number}.🙂")
    again()


def transfer():
    user = login()
    if user is None:
        again()
        return
    else:
        try:
            amount = int(input("\nHow much would you like to transfer? "))
            account_number = int(input("\nWhich account number would you like to transfer to? "))
        except ValueError:
            print("\nInvalid input!!😡")
            again()
            return

        person = user.transfer(amount, account_number)
        if person:
            record(user.email, "transfer", amount, person)
            again()
            return True
        else:
            again()
            return False


def deposit():
    user = login()
    if user is None:
        again()
        return
    else:
        try:
            amount = int(input("\nHow much would you like to deposit? "))
        except ValueError:
            print("\nInvalid input!!😡")
            again()
            return
        if amount > 999_999:
            print("\n Are you a ritualist?🤨")
            print("\n Sorry, you can't transfer more than N999,999 at a time.❌")
            again()
            return

        user.transact("deposit", amount)
        record(user.email, "deposit", amount)
        again()
        return True


def withdraw():
    user = login()
    if user is None:
        again()
        return
    else:
        try:
            amount = int(input("\nHow much would you like to withdraw? "))
        except ValueError:
            print("\nInvalid input!!😡")
            again()
            return

        status = user.transact("withdraw", amount)

        if status:
            record(user.email, "withdrawal", amount)
            again()
            return True
        else:
            again()
            return False


def check_balance():
    user = login()
    if user is None:
        again()
    else:
        user.check_balance()
        again()


def get_account_statement():
    user = login()
    if user is None:
        again()
    else:
        user.get_account_statement()
        again()


def change_password():
    user = login()
    if user is None:
        again()
    else:
        user.change_password()
        again()


def admin_start():
    user = login()
    if user is None:
        again()
        return
    elif user.role != "official":
        print("\nSorry, you don't have access to this portal!😡🤬")
        again()
        return False
    else:
        transaction = input(
            f"\nGood day {user.name}.🙂"
            "\nWhat would you like to do?\n\n"
            "1. Open an account.\n"
            "2. Edit customer details.\n"
            "3. Get customer details.\n"
            "4. Change password.\n"
            "\nReply with a number to begin transaction: "
        )
        match transaction:
            case "1":
                admin_open_account()
            case "2":
                edit_customer_details()
            case "3":
                get_customer_details()
            case "4":
                user.change_password()
                again()
            case default:
                print("\n\nSorry, invalid input!!🤬😡")
                again()


def admin_open_account():
    new_user_role = input(
        "\nWhat type of account would you like to create?"
        "\nType 'A' for an official account and 'B' for a customer account. "
    ).lower()
    match new_user_role:
        case "a":
            print("Opening account...")
            name = input("What is the name for the account? ").title()
            password1 = input("Type a password to secure your account: ")
            password2 = input("Please confirm password: ")

            if not name or not password1 or not password2:
                print("\nSorry, invalid inputs!! Make sure to fill all fields correctly!!🤬😡")
                admin_open_account()
                return

            if password1 != password2:
                print("\nSorry, passwords do not match!!😡")
                admin_open_account()
                return
            email = None
            try:
                database = pandas.read_json("database.json")
            except ValueError:
                pass
            else:
                # if email already exists in the company
                if f"{name.lower()}@bank.com" in database.columns:
                    email = f"{name.lower()}{dt.datetime.now().second}@bank.com"

            new_user = Official(name, email=email, password=password1)
            print(f"\nSuccess!! Account has been created. Email is {new_user.email}.🙂")
            again()
            return
        case "b":
            open_account()
            return
        case default:
            print("\n\nSorry, invalid input!!🤬😡")
            admin_open_account()
            return


def edit_customer_details():
    customer = input("\nEmail of user account you wish to edit: ").lower()
    try:
        database = pandas.read_json("database.json")
    except ValueError:
        print("\nSorry, email not found!!😓")
        edit_customer_details()
        return
    else:
        if customer not in database:
            print("\nSorry, email not found!!😓")
            edit_customer_details()
            return
        detail = input(
            "\nWhat detail would you like to change?\n\n"
            "1. Account number.\n"
            "2. Account type.\n"
            "3. Role.\n"
            "4. Account balance.\n"
            "5. Account name.\n"
            "6. Account email.\n"
            "Reply with a number to proceed."
        )

        with open("database.json", "w") as file:
            database = database.to_dict()
            match detail:
                case "1":
                    new_account_number = input("\nInput new account number: ")
                    database[customer]["account number"] = new_account_number
                case "2":
                    new_account_type = input(
                        "\nInput new account type. Type 's' for savings and 'c' for current."
                    ).lower()
                    if new_account_type not in ["s", "c"]:
                        print("\nSorry, invalid account type.😡🤬")
                        edit_customer_details()
                        return
                    database[customer]["account type"] = "savings" if new_account_type == "s" else "current"
                case "3":
                    new_role = input(
                        "\nInput new user role. Type 'a' for official and 'b' for customer."
                    )
                    if new_role not in ["a", "b"]:
                        print("\nSorry, invalid user role.😡🤬")
                        edit_customer_details()
                        return
                    database[customer]["role"] = "official" if new_role == "a" else "customer"
                case "4":
                    new_account_balance = input("\nInput new account balance: ")
                    try:
                        new_account_balance = int(new_account_balance)
                    except ValueError:
                        print("\nSorry, invalid input.😡🤬")
                        edit_customer_details()
                        return
                    database[customer]["balance"] = new_account_balance
                case "5":
                    new_account_name = input("\nInput new account name: ")
                    database[customer]["name"] = new_account_name
                case "6":
                    new_account_email = input("\nInput new account email: ")
                    database[customer]["email"] = new_account_email
                case default:
                    print("\n\nSorry, invalid input!!🤬😡")
                    edit_customer_details()
                    return

            json.dump(database, file, indent=4)
            print("\nDetail changed successfully!🙂")
        again()
        return


def get_customer_details():
    customer = input("\nEmail of customer you wish to see: ").lower()
    try:
        database = pandas.read_json("database.json")
    except ValueError:
        print("\nSorry, email not found!!😓")
        get_customer_details()
        return
    else:
        if customer not in database:
            print("\nSorry, email not found!!😓")
            get_customer_details()
            return
        print("\n-------------Account Details------------------")
        print(f"\n{database[customer]}")
        try:
            records = pandas.read_csv("records.csv")
        except FileNotFoundError:
            print("\nSorry, customer has not made any transactions.😑")
            again()
            return
        else:
            print("\n-------------Account Statement------------------\n")
            print(records[records.user == customer])
            again()


def again():
    another = input(
        "\nWould you like to perform another transaction? "
        "Type 'y' for yes or 'n' for no. "
    ).lower()

    match another:
        case "y":
            start()
        case "n":
            print("\nThank you and have a nice day.🙂")
        case default:
            print("\nSorry, invalid input!🤬😡")
            again()
