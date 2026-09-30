class TransactionError(Exception):
    """Custom exception for invalid transactions"""
    pass


class Account:
    def __init__(self, acc_id, balance=0):
        self.acc_id = acc_id
        self.balance = balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            raise TransactionError("Deposit amount must be positive")
        self.balance += amount
        self.history.append(f"DEPOSIT {amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise TransactionError("Withdraw amount must be positive")
        if self.balance < amount:
            raise TransactionError("Insufficient balance")
        self.balance -= amount
        self.history.append(f"WITHDRAW {amount}")

    def __str__(self):
        return f"{self.acc_id} {self.balance}"


class Bank:
    def __init__(self):
        self.accounts = {}
        self.batches = []
        self.failed_batches = []

    def add_account(self, acc_id, balance=0):
        self.accounts[acc_id] = Account(acc_id, balance)

    def transfer(self, from_acc, to_acc, amount):
        if from_acc not in self.accounts or to_acc not in self.accounts:
            raise TransactionError("Invalid account")
        self.accounts[from_acc].withdraw(amount)
        self.accounts[to_acc].deposit(amount)

    def process_batch(self, operations, batch_number):
        snapshot = {acc: self.accounts[acc].balance for acc in self.accounts}
        try:
            for op in operations:
                self.execute(op)
        except TransactionError as e:
            print(f"FAILED {batch_number} - {e}")
            # rollback
            for acc in snapshot:
                self.accounts[acc].balance = snapshot[acc]
            self.failed_batches.append(batch_number)

    def execute(self, operation):
        parts = operation.split()
        if parts[0] == "DEPOSIT":
            self.accounts[parts[1]].deposit(int(parts[2]))
        elif parts[0] == "WITHDRAW":
            self.accounts[parts[1]].withdraw(int(parts[2]))
        elif parts[0] == "TRANSFER":
            self.transfer(parts[1], parts[2], int(parts[3]))
        else:
            raise TransactionError("Unknown operation")

    def print_balances(self):
        for acc in sorted(self.accounts.keys()):
            print(self.accounts[acc])


# ---------------- SAMPLE INPUT ----------------
bank = Bank()
bank.add_account("X", 500)
bank.add_account("Y", 200)
bank.add_account("Z", 100)

# Operations outside batch
bank.execute("TRANSFER X Y 100")

# Batch 1 (will succeed)
batch1 = [
    "DEPOSIT Z 50",
    "WITHDRAW Y 100"
]
bank.process_batch(batch1, 1)

# Batch 2 (will fail and rollback)
batch2 = [
    "WITHDRAW X 1000",  # invalid, overdraft
    "DEPOSIT Y 200"
]
bank.process_batch(batch2, 2)

print("\nFinal Balances:")
bank.print_balances()
