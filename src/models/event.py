class Event:
    STATUS_TODO = "todo"
    STATUS_DONE = "done"

    def __init__(
        self,
        raw,
        calendar_id,
        start,
        summary,
        description,
        status
    ):
        self.raw = raw
        self.cid = calendar_id
        self.start = start
        self.summary = summary
        self.description = description
        self.status = status

    def __lt__(self, other):
        return (
            self.start,
            self.summary,
            self.done,
        ) < (
            other.start,
            other.summary,
            other.done,
        )
