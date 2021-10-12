from pipe.source import Source

class TodoList(Source):
    def __init__(self, children):
        super().__init__()
        self.children = children

    def _produce(self):
        for child in self.children:
            yield from child.produce()
