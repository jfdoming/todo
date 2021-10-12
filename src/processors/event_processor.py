from pipe import SENTINEL
from pipe.processor import Processor
from models.todo_item import TodoItem

class EventProcessor(Processor):
    def _process(self):
        while (item := (yield)) != SENTINEL:
            # TODO TaskTodoItem
            yield TodoItem(item.summary, item.start)
