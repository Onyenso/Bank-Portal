"""This module contains the classes used to create members of the bank."""

import json
import datetime as dt
import pandas


class Person:
    def __init__(self, name=None, password=None, email=None):
        if not name or not password:
            raise TypeError("Sorry, all fields are required!")
        self.name = name
        self.password = password
        self.email = email

    def save_to_database(self, new_detail, email):
        """A method that saves a newly created instance to the database"""
        try:
            with open("database.json", "r") as database:
                details = json.load(database)
                # This condition is to avoid creating a new user in the database via the login function
                if email in details:
                    return

        except FileNotFoundError:
            with open("database.json", "x") as database:
                json.dump(new_detail, database, indent=4)
        else:
            details.update(new_detail)
            with open("database.json", "w") as database:
                json.dump(details, database, indent=4)

        with open("member_count.txt") as file:
            member_id = file.read()

        with open("member_count.txt", "w") as file:
            file.write(f"{int(member_id) + 1}")

    def change_password(self):
        new_password = input("Type new password: ")
        new_password2 = input("Confirm new password: ")
        database = pandas.read_json("database.json")

        if new_password != new_password2:
            print("\nSorry, passwords do not match!!😡")
            return False

        with open("database.json", "w") as file:
            database = database.to_dict()
            database[self.email]["password"] = new_password
            json.dump(database, file, indent=4)
            print("\n Password changed successfully.🙂")
            return True


class Official(Person):
    def __init__(self, name=None, email=None, password=None):
        super().__init__(name, password)
        self.role = "official"
        name = self.name.replace(" ", "").lower()
        self.email = email if email else f"{name.lower()}@bank.com"
        self.salary = 100_000
        self.save_to_database(self.get_detail(), self.email)

    def get_detail(self):
        with open("member_count.txt") as file:
            member_id = file.read()

        new_detail = {
            self.email: {
                "id": member_id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "role": self.role,
            }
        }
        return new_detail


class Customer(Person):
    def __init__(self, name, email, password, account_type, balance=0):
        super().__init__(name, password)

        if not email or not account_type:
            raise TypeError("Sorry, all fields are required!")

        self.role = "customer"
        self.email = email
        self.balance = balance

        now = dt.datetime.now()

        with open("member_count.txt") as file:
            member_id = file.read()

        account_number = int(
            f"{now.microsecond}{now.second}{now.hour}"
            f"{now.weekday()}{now.day}{now.month}{now.year}{member_id}"
        )

        self.account_number = account_number

        if account_type.lower() not in ["current", "savings"]:
            raise Exception("Sorry. Account type not supported.")

        self.account_type = account_type
        self.save_to_database(self.get_detail(), self.email)

    def get_detail(self):
        with open("member_count.txt") as file:
            member_id = file.read()

        new_detail = {
            self.email: {
                "id": member_id,
                "name": self.name,
                "email": self.email,
                "password": self.password,
                "role": self.role,
                "account type": self.account_type,
                "account number": self.account_number,
                "balance": self.balance,
            }
        }
        return new_detail

    def check_balance(self):
        database = pandas.read_json("database.json")
        print(f"\nYour current account balance is N{database[self.email]['balance']}.😊")
        return

    def transfer(self, amount, account_number):
        database = pandas.read_json("database.json")
        query = (database == account_number).any()
        person = database.loc[:, query]

        # if user has less amount of funds
        if amount > database[self.email]["balance"]:
            print(f"\nCurrent user balance is: {database[self.email]['balance']}")
            print("\nSorry, insufficient funds.😓")
            return False

        # if no account was found matching the account number
        elif len(person.columns) == 0:
            print("\nSorry, account number not found.😓")
            return False
        else:
            person = person.squeeze()

            with open("database.json", "w") as file:
                database = database.to_dict()
                database[person.email]["balance"] = database[person.email]["balance"] + amount
                database[self.email]["balance"] = database[self.email]["balance"] - amount

                json.dump(database, file, indent=4)

            print(f"Success!! N{amount} has been sent to {database[person.email]['name']}!🙂")
            print(database[person.email]["name"])
            return database[person.email]["name"]

    def transact(self, operation, amount):
        database = pandas.read_json("database.json")
        with open("database.json", "w") as file:
            database = database.to_dict()
            match operation:
                case "deposit":
                    database[self.email]["balance"] = database[self.email]["balance"] + amount
                    json.dump(database, file, indent=4)
                    print(f"Success!! N{amount} has been deposited to {database[self.email]['name']}!🙂")
                    return True
                case "withdraw":
                    if database[self.email]["balance"] < amount:
                        json.dump(database, file, indent=4)
                        print("\nSorry, insufficient funds.😡🤬")
                        return False
                    else:
                        database[self.email]["balance"] = database[self.email]["balance"] - amount
                        json.dump(database, file, indent=4)
                        print(f"Success!! here is your N{amount}💵💵! Enjoy!🙂")
                        return True

    def get_account_statement(self):
        try:
            records = pandas.read_csv("records.csv")
        except FileNotFoundError:
            print("\nSorry, you have not made any transactions.😑")
        else:
            print(records[records.user == self.email])
