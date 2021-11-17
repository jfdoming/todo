from pipe import SENTINEL
from pipe.processor import Processor
from models.event import Event
from models.todo_item import TodoItem

class EventProcessor(Processor):
    def _process(self):
        while (item := (yield)) != SENTINEL:
            # TODO TaskTodoItem
            if item.status == Event.STATUS_DONE:
                yield
                continue
            yield TodoItem(item.summary, item.start)
