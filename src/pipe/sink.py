from abc import ABC, abstractmethod

class Sink(ABC):
    @abstractmethod
    def consume(self):
        yield
