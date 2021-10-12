from abc import ABC, abstractmethod

SENTINEL = object()

class Source(ABC):
    def __init__(self):
        self._children = []

    @abstractmethod
    def produce(self):
        yield

    def __rshift__(self, other):
        self._children.append(other)
        return other

    def __repeat(self):
        x = yield
        while True:
            x = yield x

    def send_to_pipe(self):
        sender = self.produce()

        receivers = [child.consume() for child in self._children]

        next(sender)
        for child in receivers:
            next(child)

        for item in sender:
            for child in receivers:
                child.send(item)
        for child in receivers:
            child.send(SENTINEL)
