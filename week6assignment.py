def log_operation(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if result:
            print(f"[OK] {func.__name__} succesful")
        else:
            print(f"[FAIL] {func.__name__} denied")
    return wrapper

class Book:
    _library = []
    def __init__(self, title, total_copies):
        self.title = title
        self.total_copies = total_copies
        self._borrowed = 0
        Book._library.append(self)
    
    @log_operation
    def borrow(self):
        if self._borrowed == self.total_copies:
            return False
        self._borrowed += 1
        return True
    
    @log_operation
    def return_book(self):
        if self._borrowed == 0:
            return False
        self._borrowed -= 1
        return True
    
    def available(self):
        return self.total_copies - self._borrowed
    
    def usage_percent(self):
        percentage = (self._borrowed / self.total_copies) * 100
        return round(percentage, 1)

    @classmethod
    def from_entry(cls, entry):
        title, copies = entry.split(":")
        copies = int(copies)
        return Book(title, copies)
    
    @staticmethod
    def is_valid_isbn(isbn):
        return len(isbn) == 13 and isbn.isnumeric()
    
    @classmethod
    def total_available(cls):
        total = 0
        for book in cls._library:
            total += book.available()
        return total
            
b1 = Book("Data Structures", 2)
b2 = Book.from_entry("Algorithms:3")

b1.borrow()
b1.borrow()
b1.borrow()
b1.return_book()

b2.borrow()
b2.return_book()
b2.return_book()

print(f"{b1.title}: available = {b1.available()}, usage = {b1.usage_percent()}%")
print(f"{b2.title}: available = {b2.available()}, usage = {b2.usage_percent()}%")

print(f"Valid ISBN '9781234567890': {Book.is_valid_isbn('9781234567890')}")
print(f"Valid ISBN '978-12345': {Book.is_valid_isbn('978-12345')}")
print(f"Total available in library: {Book.total_available()}")