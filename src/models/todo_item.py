class TodoItem:
    def __init__(self, summary, deadline=None):
        self.summary = summary
        self.deadline = deadline

    def __lt__(self, other):
        if self.deadline is None and other.deadline is None:
            return self.summary < other.summary
        if self.deadline is None:
            return True
        if other.deadline is None:
            return False
        return (self.deadline, self.summary) < (other.deadline, other.summary)
