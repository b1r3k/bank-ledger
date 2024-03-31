from decimal import Decimal
from unittest import TestCase

from bank_ledger.account import Account
from bank_ledger.transaction import GENESIS_TRANSACTION, Transaction


class TestTransactions(TestCase):
    def test_transaction_creation(self):
        transaction = Transaction(Decimal(10.0), 0, GENESIS_TRANSACTION.hash)
        self.assertEqual(transaction.hash, "48c0126ee8b0d96db49235fc1bcdccd783ed1a551a0e0c15846cd667c3e0d8b3")

    def test_transaction_list_append(self):
        transaction = Transaction(Decimal(10.0), 0, GENESIS_TRANSACTION.hash)
        transaction_list = [transaction]
        self.assertEqual(len(transaction_list), 1)


class TestAccount(TestCase):
    def test_account_creation(self):
        account = Account("Bob")
        self.assertEqual(account.name, "Bob")

    def test_deposit(self):
        account = Account("Bob")
        account.deposit(Decimal(10.0))
        self.assertEqual(account.balance, Decimal(10.0))

    def test_withdraw(self):
        account = Account("Bob")
        account.deposit(Decimal(10.0))
        account.withdraw(Decimal(5.0))
        self.assertEqual(account.balance, Decimal(5.0))

    def test_transfer(self):
        bob = Account("Bob")
        alice = Account("Alice")
        bob.deposit(Decimal(10.0))
        bob.transfer(Decimal(5.0), alice)
        self.assertEqual(bob.balance, Decimal(5.0))
        self.assertEqual(alice.balance, Decimal(5.0))

    def test_withdraw_negative(self):
        account = Account("Bob")
        with self.assertRaises(AssertionError):
            account.withdraw(-Decimal(5.0))

    def test_deposit_negative(self):
        account = Account("Bob")
        with self.assertRaises(AssertionError):
            account.deposit(-Decimal(5.0))

    def test_withdraw_more_than_balance(self):
        account = Account("Bob")
        account.deposit(Decimal(10.0))
        with self.assertRaises(AssertionError):
            account.withdraw(Decimal(15.0))
