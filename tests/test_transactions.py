from decimal import Decimal
from unittest import TestCase

from bank_ledger.account import Account
from bank_ledger.transaction import (
    GENESIS_TRANSACTION,
    Ledger,
    Transaction,
    validate_transaction,
)


class TestTransactions(TestCase):
    def test_transaction_creation(self):
        transaction = Transaction("aaa", Decimal(10.0), 0, GENESIS_TRANSACTION.hash)
        self.assertEqual(transaction.hash, "66439fff94e17c67331c96c75fbf774b3d9f0400ebefbf1db5f7141adccd4767")

    def test_transaction_list_append(self):
        transaction = Transaction("aaa", Decimal(10.0), 0, GENESIS_TRANSACTION.hash)
        transaction_list = [transaction]
        self.assertEqual(len(transaction_list), 1)


class TestLedger(TestCase):
    def setUp(self):
        self.ledger = Ledger()

    def test_transaction_validation(self):
        t1 = self.ledger.new_transaction("aaa", Decimal(10.0))
        t2 = self.ledger.new_transaction("aaa", Decimal(5.0))
        self.assertTrue(validate_transaction(t1, t2))

    def test_transaction_validation_fails(self):
        t1 = self.ledger.new_transaction("aaa", Decimal(10.0))
        t2 = self.ledger.new_transaction("aaa", Decimal(5.0))
        t2.amount = Decimal(6.0)
        self.assertFalse(validate_transaction(t2, t1))

    def test_transaction_verification(self):
        self.ledger.new_transaction("aaa", Decimal(10.0))
        self.ledger.new_transaction("aaa", Decimal(5.0))
        self.assertTrue(self.ledger.verify())

    def test_transaction_verification_fails(self):
        self.ledger.new_transaction("aaa", Decimal(10.0))
        self.ledger.new_transaction("aaa", Decimal(5.0))
        self.ledger._transactions[1].amount = Decimal(6.0)
        with self.assertRaises(ValueError):
            self.ledger.verify()


class TestAccount(TestCase):
    def setUp(self):
        self.ledger = Ledger()
        self.bob_account = Account("Bob", self.ledger)
        self.alice_account = Account("Alice", self.ledger)

    def test_account_creation(self):
        self.assertEqual(self.bob_account.name, "Bob")

    def test_deposit(self):
        self.bob_account.deposit(Decimal(10.0))
        self.assertEqual(self.bob_account.balance, Decimal(10.0))

    def test_withdraw(self):
        self.bob_account.deposit(Decimal(10.0))
        self.bob_account.withdraw(Decimal(5.0))
        self.assertEqual(self.bob_account.balance, Decimal(5.0))

    def test_transfer(self):
        self.bob_account.deposit(Decimal(10.0))
        self.bob_account.transfer(Decimal(5.0), self.alice_account)
        self.assertEqual(self.bob_account.balance, Decimal(5.0))
        self.assertEqual(self.alice_account.balance, Decimal(5.0))

    def test_withdraw_negative(self):
        with self.assertRaises(AssertionError):
            self.bob_account.withdraw(-Decimal(5.0))

    def test_deposit_negative(self):
        with self.assertRaises(AssertionError):
            self.bob_account.deposit(-Decimal(5.0))

    def test_withdraw_more_than_balance(self):
        self.bob_account.deposit(Decimal(10.0))
        with self.assertRaises(AssertionError):
            self.bob_account.withdraw(Decimal(15.0))

    def test_blocked_account_deposit(self):
        self.bob_account.block()
        with self.assertRaises(AssertionError):
            self.bob_account.deposit(Decimal(10.0))
