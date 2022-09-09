import pandas
import json
import datetime as dt
import os

# with open("database.json") as file:
#     data = json.load(file)
    # print((data))

# df = pandas.read_json("database.json")

# print(df["uchenna@gmail.com"]["email"])

# query = (df == 64812181405920225).any()
#
# sub_df = df.loc[:, query]

# series = sub_df.squeeze()
# print(series.balance)
# series.update(pandas.Series([500], index=["balance"]))
# # print(series["balance"])
# print((df.to_dict()))
now = dt.datetime.now()
# print(now.date(), now.hour, now.minute)
test_users = {
    "test1@gmail.com": {
        "id": "1",
        "name": "Test 1",
        "email": "test1@gmail.com",
        "password": "ass",
        "role": "customer",
        "account number": 276053591127920222,
        "account type": "savings",
        "balance": 14500
    },
    "test2@bank.com": {
        "id": "2",
        "name": "Test 2",
        "email": "test2@bank.com",
        "password": "qwerty",
        "role": "official",
        "account number": "",
        "account type": "",
        "balance": ""
    }
}

# os.rename("non_existent.json", "database.json")
# with open("database.json") as file:
#     print(file.readlines())
