import time
from decimal import Decimal
from hashlib import sha256


class Transaction:
    def __init__(self, amount: Decimal, timestamp: int, prev_transaction_hash: str):
        self.amount = amount
        self.timestamp = timestamp
        self.previous_transaction = prev_transaction_hash
        self.hash = self.__hash__()

    def __str__(self):
        return f"{self.timestamp}:{self.amount}:{self.previous_transaction}"

    def __hash__(self):
        return sha256(str(self).encode()).hexdigest()


GENESIS_TRANSACTION = Transaction(Decimal(0), 0, sha256("troi".encode()).hexdigest())


class Ledger:
    def __init__(self):
        self._transactions = (GENESIS_TRANSACTION,)

    def new_transaction(self, amount: Decimal):
        new_transaction = Transaction(amount, int(time.time()), self._transactions[-1].hash)
        self._transactions += (new_transaction,)
        return new_transaction

    def __str__(self):
        return "\n".join([str(transaction) for transaction in self._transactions])
