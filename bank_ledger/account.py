from decimal import Decimal
from enum import Enum, auto

from .transaction import Ledger


class AccountStatusEnum(Enum):
    ACTIVE = auto()
    BLOCKED = auto()


class Account:
    def __init__(self, name):
        self.name = name
        self._ledger = Ledger()
        self._status = AccountStatusEnum.ACTIVE

    def deposit(self, amount: Decimal):
        assert amount > 0, "Cannot deposit negative amounts"
        assert not self.is_blocked, "Account is blocked"
        self._ledger.new_transaction(amount)

    def withdraw(self, amount: Decimal):
        assert amount > 0, "Cannot withdraw negative amounts"
        assert self.balance >= amount, "Insufficient funds"
        assert not self.is_blocked, "Account is blocked"
        self._ledger.new_transaction(-1 * amount)

    def transfer(self, amount, target: "Account"):
        self.withdraw(amount)
        target.deposit(amount)

    def block(self):
        self._status = AccountStatusEnum.BLOCKED

    @property
    def balance(self):
        return sum([transaction.amount for transaction in self._ledger.transactions])

    @property
    def is_blocked(self):
        return self._status == AccountStatusEnum.BLOCKED

    def __str__(self):
        return f"{self.name} has {self.balance}"
