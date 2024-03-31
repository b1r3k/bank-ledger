import time
from decimal import Decimal
from hashlib import sha256


# TODO: probably good case for pydantic
class Transaction:
    def __init__(self, owner: str, amount: Decimal, timestamp: int, prev_transaction_hash: str):
        self.owner = owner
        self.amount = amount
        self.timestamp = timestamp
        self.prev_transaction_hash = prev_transaction_hash
        self.hash = self.__hash__()

    def __str__(self):
        return f"{self.timestamp}:{self.owner}:{self.amount}:{self.prev_transaction_hash}"

    def __hash__(self):
        return sha256(str(self).encode()).hexdigest()


GENESIS_TRANSACTION = Transaction("penelope", Decimal(0), 0, sha256("troi".encode()).hexdigest())


def validate_transaction(prev_transaction: Transaction, transaction: Transaction):
    """
    Validate a transaction meaning if transaction hash is correct because it should base on prev_transaction hash

    :param prev_transaction:
    :param transaction:
    :return: True if transaction is valid, False otherwise
    """
    hypothetical = Transaction(transaction.owner, transaction.amount, transaction.timestamp, prev_transaction.hash)
    return hypothetical.hash == transaction.hash


class Ledger:
    def __init__(self):
        self._transactions = (GENESIS_TRANSACTION,)

    @property
    def transactions(self):
        return self._transactions

    def new_transaction(self, owner: str, amount: Decimal):
        new_transaction = Transaction(owner, amount, int(time.time()), self._transactions[-1].hash)
        self._transactions += (new_transaction,)
        return new_transaction

    def verify(self):
        for i in range(1, len(self._transactions)):
            if validate_transaction(self._transactions[i - 1], self._transactions[i]) is False:
                raise ValueError(f"Transaction {self._transactions[i]} is invalid")
        return True

    def get_account_transactions(self, account_id):
        for transaction in self._transactions:
            if transaction.owner == account_id:
                yield transaction

    def __str__(self):
        return "\n".join([str(transaction) for transaction in self._transactions])

    def __hash__(self):
        return hash(self._transactions)
