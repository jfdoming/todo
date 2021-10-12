from todo_list import TodoList

class TodoGroup(TodoList):
    def __init__(self, children):
        super().__init__()
        self.children = children

    def list(self):
        for child in self.children:
            yield from child.list()
