from pipe import SENTINEL
from pipe.sink import Sink
from models.todo_list import TodoList

class TodoListCollector(Sink):
    def _consume(self):
        todos = []

        while (item := (yield)) != SENTINEL:
            if item is None:
                continue
            todos.append(item)

        todos.sort()
        yield TodoList(todos[:10])
