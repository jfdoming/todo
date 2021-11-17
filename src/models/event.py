class Event:
    STATUS_TODO = "todo"
    STATUS_DONE = "done"

    def __init__(self, summary, start, status):
        self.summary = summary
        self.start = start
        self.status = status

    def __lt__(self, other):
        return (self.start, self.summary, self.done) < (other.start, other.summary, other.done)
