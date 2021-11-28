from pipe import SENTINEL
from pipe.sink import Sink
from models.todo_list import TodoList

class DoneCollector(Sink):
    def __init__(self, api, done):
        self.api = api
        self.done = set(done)

    def _consume(self):
        events = []

        while (item := (yield)) != SENTINEL:
            if item is None:
                continue
            item_hash_digest = f"{hash(item):0{16}x}"
            if item_hash_digest in self.done:
                events.append(item.event_source)

        self.api.batch_mark_done(events)
