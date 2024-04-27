from abc import abstractmethod

from pipe import SENTINEL, SKIP
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
        consume = self._send_to_pipe([self, self.produce()])

        item_map = self.process()

        while (item := (yield)) != SENTINEL:
            item = item_map.send(item)
            if item is not SKIP:
                for child in receivers:
                    child.send(item)
            next(item_map)

        results = [
            result for result_list in (
                Source._terminate(child)
                for child in receivers
            ) if result_list is not None and not print("result_list:", result_list)
            for result in result_list
        ]

        print("processor result:", results)
        yield results

    def _produce(self):
        yield
