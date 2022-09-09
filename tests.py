import json
import unittest
import random
import utilities
import os
import pandas
from member_factory import Official, Customer
from unittest import TestCase, mock


class TestUtilities(TestCase):
    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_login_customer_with_correct_detail(self, mocked_input):
        """Tests that a right email and password for a customer returns a Customer object"""
        mocked_input.side_effect = ["test1@gmail.com", "ass"]
        self.assertIsInstance(utilities.login(), Customer)

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_login_official_with_correct_detail(self, mocked_input):
        """Tests that a right email or password for an official returns an Official object"""
        mocked_input.side_effect = ["test2@bank.com", "qwerty"]
        self.assertIsInstance(utilities.login(), Official)

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_login_with_wrong_detail(self, mocked_input):
        """Tests that a wrong email or password returns None"""
        mocked_input.side_effect = ["test1@gmail.com", "ss"]
        self.assertEqual(utilities.login(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipIf(os.path.exists("database.json"), "Test only runs when database does not exist.")
    def test_login_no_database(self, mocked_input):
        """Tests that None is returned when there is no database"""
        mocked_input.side_effect = ["test1@gmail.com", "ass"]
        self.assertEqual(utilities.login(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_open_account_with_correct_details(self, mocked_input):
        """Tests that a new user is created and saved to the database"""
        mocked_input.side_effect = ["John Doe", "johndoe@gmail.com", "c", "pass123", "pass123", "n"]
        utilities.open_account()
        database = pandas.read_json("database.json")
        self.assertIn("johndoe@gmail.com", database, "Expected johndoe@gmail.com to be in database.")
        # Remove false data that was created in database
        with open("database.json", "w") as file:
            database = database.to_dict()
            del database["johndoe@gmail.com"]
            json.dump(database, file, indent=4)

    @mock.patch("utilities.input", create=True)
    def test_open_account_with_invalid_input(self, mocked_input):
        """Tests that a user is not created if inputs are invalid"""
        inputs = ["John Doe", "johndoe@gmail.com", "s", "pass123", "pass123", "n"]
        # make a random input to be invalid
        inputs[random.randint(0, 4)] = ""
        mocked_input.side_effect = inputs
        self.assertEqual(utilities.open_account(), None, "Expected None.")

    @mock.patch("utilities.input", create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_open_account_with_already_existing_email(self, mocked_input):
        """Tests that user is not created with an already existing email"""
        database = pandas.read_json("database.json")
        # get random email from database
        email = random.choice(database.columns)
        mocked_input.side_effect = ["John Doe", email, "s", "pass123", "pass123", "n"]
        self.assertEqual(utilities.open_account(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_deposit_with_correct_inputs(self, mocked_input):
        """Tests that a deposit is made when there is correct input"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "1000", "n"]
        self.assertEqual(utilities.deposit(), True, "Expected True.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_deposit_with_incorrect_amount(self, mocked_input):
        """Tests that a deposit is NOT made when an incorrect amount is given"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "invalid_amount", "n"]
        self.assertEqual(utilities.deposit(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_deposit_with_amount_greater_than_999_999(self, mocked_input):
        """Tests that a deposit is NOT made when an incorrect amount is given"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "1_000_000", "n"]
        self.assertEqual(utilities.deposit(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_withdraw_with_correct_inputs(self, mocked_input):
        """Tests that a withdrawal is made when there is correct input"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "1000", "n"]
        self.assertEqual(utilities.withdraw(), True, "Expected True.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_withdraw_with_incorrect_inputs(self, mocked_input):
        """Tests that a withdrawal is NOT made when there is incorrect input"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "invalid_amount", "n"]
        self.assertEqual(utilities.withdraw(), None, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_withdraw_with_insufficient_funds(self, mocked_input):
        """Tests that a withdrawal is NOT made when there is insufficient funds"""
        database = pandas.read_json("database.json")
        test_user_balance = database["test1@gmail.com"]["balance"]
        mocked_input.side_effect = ["test1@gmail.com", "ass", f"{test_user_balance + 1}", "n"]
        self.assertEqual(utilities.withdraw(), False, "Expected None.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_admin_start_for_non_official_user(self, mocked_input):
        """Tests that the admin portal is not accessible to non officials"""
        mocked_input.side_effect = ["test1@gmail.com", "ass", "n"]
        self.assertEqual(utilities.admin_start(), False, "Expected False.")

    @mock.patch('utilities.input', create=True)
    @unittest.skipUnless(os.path.exists("database.json"), "Test only runs when database exists.")
    def test_admin_open_account_with_correct_details(self, mocked_input):
        """Tests that a new user is created and saved to the database through the admin portal"""
        mocked_input.side_effect = ["A", "John Doe", "pass123", "pass123", "n"]
        utilities.admin_open_account()
        database = pandas.read_json("database.json")
        self.assertIn("johndoe@bank.com", database, "Expected johndoe@bank.com to be in database.")
        # Remove false data that was created in database
        with open("database.json", "w") as file:
            database = database.to_dict()
            del database["johndoe@bank.com"]
            json.dump(database, file, indent=4)

    """And so on and so forth"""
