from abc import abstractmethod

from pipe.source import SENTINEL
from pipe.source import Source
from pipe.sink import Sink

class Processor(Source, Sink):
    @abstractmethod
    def process(self):
        yield

    def consume(self):
        item_map = self.process()

        receivers = [child.consume() for child in self._children]

        for child in receivers:
            next(child)
        next(item_map)

        while (item := (yield)) != SENTINEL:
            item = item_map.send(item)
            for child in receivers:
                child.send(item)
            next(item_map)
        for child in receivers:
            child.send(SENTINEL)

        yield

    def produce(self):
        yield
