from abc import abstractmethod

from pipe.source import Source

class TodoList(Source):
    @abstractmethod
    def list(self):
        pass

    def produce(self):
        yield from self.list()

