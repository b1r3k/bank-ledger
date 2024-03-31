from decimal import Decimal

from .transaction import Ledger


class Account:
    def __init__(self, name):
        self.name = name
        self._ledger = Ledger()

    def deposit(self, amount: Decimal):
        assert amount > 0, "Cannot deposit negative amounts"
        self._ledger.new_transaction(amount)

    def withdraw(self, amount: Decimal):
        assert amount > 0, "Cannot withdraw negative amounts"
        assert self.balance >= amount, "Insufficient funds"
        self._ledger.new_transaction(-1 * amount)

    def transfer(self, amount, target: "Account"):
        self.withdraw(amount)
        target.deposit(amount)

    @property
    def balance(self):
        return sum([transaction.amount for transaction in self._ledger._transactions])

    def __str__(self):
        return f"{self.name} has {self.balance}"
