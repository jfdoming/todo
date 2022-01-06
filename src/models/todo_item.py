import hashlib

from config import CONFIG
from pipe.source import Source
from models.todo_type import TodoType

class TodoItem(Source):
    def __init__(self, summary, deadline=None, event_source=None):
        self.summary = summary
        self.deadline = deadline
        self.event_source = event_source

        self.course = None
        if self.event_source is not None:
            parts = summary.split()
            if len(parts) >= 3 and parts[0].isalpha() and parts[1].isdigit():
                parts = parts[:2]
                course = "".join(parts)
                if course in CONFIG.courses:
                    self.course = course

        self.type = TodoType.from_summary(self.summary)

    def __lt__(self, other):
        if self.deadline is None and other.deadline is None:
            return self.summary < other.summary
        if self.deadline is None:
            return True
        if other.deadline is None:
            return False
        return (self.deadline, self.summary) < (other.deadline, other.summary)

    def _produce(self):
        yield self

    def __hash__(self):
        m = hashlib.md5()
        m.update(self.summary.encode())
        m.update(str(self.deadline).encode())
        return int(m.hexdigest(), 16)
