from itertools import islice

from models.todo_group import TodoGroup

class PrimaryTodoList(TodoGroup):
    def list(self):
        yield from islice(sorted(super().list()), 10)
