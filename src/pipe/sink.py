from abc import ABC, abstractmethod

from utils.single_iter import single_iter

class Sink(ABC):
    @abstractmethod
    def _consume(self):
        yield

    @single_iter
    def consume(self):
        yield from self._consume()
