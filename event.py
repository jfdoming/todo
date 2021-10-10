class Event:
    def __init__(self, summary, start):
        self.summary = summary
        self.start = start

    def __lt__(self, other):
        return (self.start, self.summary) < (other.start, other.summary)
