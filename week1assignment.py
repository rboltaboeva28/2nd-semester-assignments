class DigitalWallet:
    service_name = "PayWay"
    min_balance = 0
    total_wallets = 0

    def __init__(self, owner, balance=0, history=None):
        self.owner = owner
        self.balance = balance
        self.history = history if history is not None else []

        DigitalWallet.total_wallets += 1

    def add_funds(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(f" + {amount}")
            print(f"Added {amount}. Balance: {self.balance}")
    
    def spend(self, amount):
        if self.balance - amount >= DigitalWallet.min_balance:
            self.balance -= amount
            self.history.append(f" - {amount}")
            print(f"Spent {amount}. Balance: {self.balance}")
        else:
            print("Insufficient balance")

    def display_wallet(self):
        print(f"Owner: {self.owner}, Balance: {self.balance}, Service: {DigitalWallet.service_name}")

    def show_history(self):
        for line in self.history:
            print(line)

wallet = DigitalWallet("Umida", 40)

wallet.display_wallet()
wallet.add_funds(25)
wallet.spend(50)
wallet.spend(10)

wallet.show_history()
print(f"Total wallets: {DigitalWallet.total_wallets}")