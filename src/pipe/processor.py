from abc import abstractmethod

from pipe import SENTINEL
from pipe.source import Source
from pipe.sink import Sink
from utils.single_iter import single_iter

class Processor(Source, Sink):
    @abstractmethod
    def _process(self):
        yield

    @single_iter
    def process(self):
        yield from self._process()

    def _consume(self):
        item_map = self.process()

        receivers = [child.consume() for child in self._children]

        while (item := (yield)) != SENTINEL:
            item = item_map.send(item)
            for child in receivers:
                child.send(item)
            next(item_map)

        results = [
            result for result in (
                result_list
                for result_list in (
                    Source._terminate(child)
                    for child in receivers
                )
                if result_list is not None
            )
        ]

        yield results

    def _produce(self):
        yield
