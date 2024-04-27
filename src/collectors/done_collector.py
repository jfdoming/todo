from pipe import SENTINEL
from pipe.sink import Sink
from models.todo_list import TodoList

class DoneCollector(Sink):
    def __init__(self, api):
        self.api = api

    def _consume(self):
        events = []

        while (item := (yield)) != SENTINEL:
            if item is None:
                continue
            events.append(item.event_source)

        self.api.batch_mark_done(events)
