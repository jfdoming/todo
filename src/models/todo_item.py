import hashlib

from pipe.source import Source
from models.todo_type import TodoType

class TodoItem(Source):
    def __init__(self, summary, deadline=None, event_source=None):
        self.summary = summary
        self.deadline = deadline
        self.event_source = event_source

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
