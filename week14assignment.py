from enum import Enum
from abc import ABC, abstractmethod

class Chart:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.notes = []
        return cls._instance
    
    def record(self, text):
        self.notes.append(text)
        print(f"(+) {text}")

class StaffKind(Enum):
    NURSE = 1
    DOCTOR = 2
    OBSERVER = 3

class Protocol(ABC):
    @abstractmethod
    def assess(self, bpm):
        pass

class BradyAlert(Protocol):
    def __init__(self, limit):
        self.limit = limit
    
    def assess(self, bpm):
        return "BRADY" if bpm < self.limit else None
    
class TachyAlert(Protocol):
    def __init__(self, limit):
        self.limit = limit
    
    def assess(self, bpm):
        return "TACHY" if bpm > self.limit else None

class Quiet(Protocol):
    def assess(self, bpm):
        return None
    
class Watcher(ABC):
    @abstractmethod
    def examine(self, bpm):
        pass

class Staff(Watcher):
    def __init__(self, name, protocol:Protocol):
        self.name = name
        self.protocol = protocol

    def examine(self, bpm):
        result = self.protocol.assess(bpm)
        if result is not None:
            Chart().record(f"{self.name} {result} (bpm={bpm})")
        return

class Patient:
    def __init__(self):
        self._watchers = []

    def assign(self, watcher):
        self._watchers.append(watcher)

    def vitals(self, bpm):
        Chart().record(f"bpm={bpm}")
        for watcher in self._watchers:
            watcher.examine(bpm)

def make_nurse(name):
    return Staff(name, BradyAlert(50))

def make_doctor(name):
    return Staff(name, TachyAlert(120))

def make_observer(name):
    return Staff(name, Quiet())

class StaffFactory:
    _builders = {
        StaffKind.NURSE: make_nurse,
        StaffKind.DOCTOR: make_doctor,
        StaffKind.OBSERVER: make_observer
    }

    @staticmethod
    def create(kind, name):
        if kind not in StaffFactory._builders:
            raise ValueError(f"Unknown staff: {kind}")
        staff = StaffFactory._builders[kind]
        return staff(name)
    
patient = Patient()
patient.assign(StaffFactory.create(StaffKind.NURSE, "Harry"))
patient.assign(StaffFactory.create(StaffKind.DOCTOR, "Hermione"))
patient.assign(StaffFactory.create(StaffKind.OBSERVER, "Ron"))

for bpm in [75, 35, 90, 130]:
    patient.vitals(bpm)

print(f"Total notes: {len(Chart().notes)}")