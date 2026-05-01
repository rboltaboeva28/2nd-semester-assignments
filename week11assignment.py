from dataclasses import dataclass, field
from contextlib import contextmanager

class LogError(Exception):
    pass

@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    response_time: int
    _status: str = field(init=False)

    def __post_init__(self):
        self._status = "PENDING"
        if self.level not in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise LogError(f"Unknown level: {self.level}")
        if self.response_time < 0:
            raise LogError
        
    @property
    def is_slow(self):
        return self.response_time > 500
    
    def __str__(self):
        return f"{self.timestamp} [{self.level}] {self.message} ({self.response_time}ms) -> {self._status}"

    def __gt__(self, other):
        if isinstance(other, LogEntry):
            return self.response_time > other.response_time
        return NotImplemented
    
class LogScanner:
    def __init__(self, entries, max_ms):
        self.entries = entries
        self.max_ms = max_ms
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current == len(self.entries):
            raise StopIteration
        entry = self.entries[self.current]
        if entry.response_time < self.max_ms:
            entry._status = "OK"
        else:
            entry._status = "ALERT"
        self.current += 1
        return entry
    
def scan_report(scanner):
    ok_entry = 0
    alert_entry = 0
    for entry in scanner:
        if entry._status == "OK":
            ok_entry += 1
        else:
            alert_entry += 1
        yield str(entry)
    yield f"Result: {ok_entry} ok, {alert_entry} alerts"

@contextmanager
def monitoring_session(name):
    try:
        print(f"[START] {name}")
        entries = []
        yield entries
    except LogError as e:
        print(f"[FAIL] {e}")
    finally:
        print(f"[END] {name} ({len(entries)} entries)")

with monitoring_session("Web Server") as logs:
    logs.append(LogEntry("10:00:01", "INFO", "GET /home", 120))
    logs.append(LogEntry("10:00:02", "WARNING", "GET /api", 850))
    logs.append(LogEntry("10:00:03", "ERROR", "POST /login", 1500))

    for line in scan_report(LogScanner(logs, 1000)):
        print(line)

    print(logs[1] > logs[0])

print()

with monitoring_session("DB Server") as logs:
    logs.append(LogEntry("11:00:01", "DEBUG", "Query", 50))