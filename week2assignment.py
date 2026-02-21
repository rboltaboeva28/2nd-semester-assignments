class ParkingLot:
    def __init__(self, name, total_spaces, occupied_spaces=0):
        self._name = name
        self.total_spaces = total_spaces
        self.occupied_spaces = occupied_spaces

    @property
    def name(self):
        return self._name
    
    @property
    def total_spaces(self):
        return self._total_spaces
    
    @total_spaces.setter
    def total_spaces(self, value):
        if value < 1:
            raise ValueError("Total spaces must be at least 1")
        self._total_spaces = value
    
    @property
    def occupied_spaces(self):
        return self._occupied_spaces
    
    @occupied_spaces.setter
    def occupied_spaces(self, value):
        if value < 0:
            raise ValueError("Occupied spaces cannot be negative")
        if value > self._total_spaces:
            raise ValueError("Occupied spaces cannot exceed total spaces")
        self._occupied_spaces = value

    @property
    def free_spaces(self):
        return self.total_spaces - self.occupied_spaces
    
    @property
    def occupancy_rate(self):
        rate = (self.occupied_spaces / self.total_spaces) * 100
        return round(rate, 1)
    
    def park(self, cars):
        if cars <= 0:
            raise ValueError("Number of cars must be positive")
        if cars > (self.total_spaces - self.occupied_spaces):
            raise ValueError("Not enough free spaces")
        self.occupied_spaces += cars

    def leave(self, cars):
        if cars <= 0:
            raise ValueError("Number of cars must be positive")
        if cars > self.occupied_spaces:
            raise ValueError("Cannot remove more cars than parked")
        self.occupied_spaces -= cars


lot = ParkingLot("Central", 30)
print(lot.name, lot.free_spaces, lot.occupancy_rate)

lot.park(20)
print(lot.occupied_spaces, lot.occupancy_rate)

lot.leave(5)
print(lot.free_spaces)

try:
    lot.park(20)
except ValueError as e:
    print(e)

try:
    lot.name = "X"
except AttributeError:
    print("Cannot change lot name")