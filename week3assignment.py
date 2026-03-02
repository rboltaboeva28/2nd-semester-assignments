class CargoTrain:
    def __init__(self, train_id):
        self.train_id = train_id
        self.cars = []

    def add_car(self, weight):
        self.cars.append(weight)

    def __len__(self):
        return len(self.cars)
    
    def __str__(self):
        return f"Train {self.train_id} with {len(self)} cars"
    
    def __repr__(self):
        return f"CargoTrain('{self.train_id}')"
    
    def __add__(self, other):
        if isinstance(other, CargoTrain):
            new_id = f"{self.train_id}-{other.train_id}"
            new_train = CargoTrain(new_id)
            new_train.cars = self.cars + other.cars
            return new_train
        return NotImplemented
            
    def __eq__(self, other):
        if isinstance(other, CargoTrain):
            return len(self.cars) == len(other.cars)
        return NotImplemented
        
    def __bool__(self):
        return len(self.cars) >= 1

t1 = CargoTrain("Express")
t1.add_car(50)
t1.add_car(40)

t2 = CargoTrain("Local")
t2.add_car(30)

t4 = CargoTrain("Empty")

print(str(t1))
print(repr(t1))
print(len(t1))

t3 = t1 + t2
print(str(t3))
print(t3.cars)

print(t1 == t2)
print(bool(t1))
print(bool(t4))