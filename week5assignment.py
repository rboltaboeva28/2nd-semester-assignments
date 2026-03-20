from abc import ABC, abstractmethod
class Taxable(ABC):
    @abstractmethod
    def tax_amount(self):
        pass

class Describable(ABC):
    @abstractmethod
    def describe(self):
        pass

class Product(Taxable, Describable):
    def __init__(self, name, price):
        self.name = name
        if price < 0:
            raise ValueError(f"Invalid price: {price}")
        self.price = price

    def tax_amount(self):
        result = round(self.price * 0.10, 2)
        return result
    
    def describe(self):
        result =  f"{self.name}: ${self.price:.2f}"
        return result
    
class DiscountedProduct(Product):
    def __init__(self, name, price, discount):
        super().__init__(name, price)
        self.discount = discount

    def final_price(self):
        result =  round(self.price * (1 - self.discount), 2)
        return result
    
    def tax_amount(self):
        result = self.final_price() * 0.1
        return result
    
    def describe(self):
        result = f"{super().describe()} -> ${self.final_price():.2f} (-{int(self.discount * 100)}%)"
        return result
    
class ImportedProduct(Product):
    def __init__(self, name, price, import_duty):
        super().__init__(name, price)
        self.import_duty = import_duty

    def tax_amount(self):
        result = round(self.price * 0.10 + self.price * self.import_duty, 2)
        return result
    
    def describe(self):
        result = f"{self.name}: ${self.price:.2f} (imported, duty {int(self.import_duty * 100)}%)"
        return result
    
class GiftCard:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def tax_amount(self):
        result = 0.0
        return result
    
    def describe(self):
        result = f"{self.name}: ${self.price:.2f} (gift card, tax-free)"
        return result
    
class Receipt:
    def __init__(self):
        self.lines = []

    def add_line(self, description, tax):
        self.lines.append((description, tax))

    def print_receipt(self):
        for line in self.lines:
            print(f"  {line[0]} | tax: ${line[1]:.2f}")

class ShoppingCart:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.items = []
        self.receipt = Receipt()
    
    def add_item(self, item):
        self.items.append(item)

    def checkout(self):
        subtotal = 0
        grand_total = 0
        total_tax = 0
        print(f"Checkout for {self.customer_name}")
        for item in self.items:
            description = item.describe()
            tax = item.tax_amount()
            self.receipt.add_line(description, tax)
            total_tax += tax
            subtotal += item.price
        grand_total = subtotal + total_tax
        self.receipt.print_receipt()
        
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Total Tax: ${total_tax:.2f}")
        print(f"Grand Total: ${grand_total:.2f}")

cart = ShoppingCart('Alisher')

cart.add_item(Product('Laptop', 1000))
cart.add_item(DiscountedProduct('Headphones', 200, 0.25))
cart.add_item(ImportedProduct('Chocolate', 10, 0.15))
cart.add_item(GiftCard('Steam Card', 50))

try:
    cart.add_item(Product('Bad Item', -5))
except ValueError as e:
    print(f'Skipped: {e}')

cart.checkout()

try:
    t = Taxable()
except TypeError:
    print('Cannot instantiate abstract class')