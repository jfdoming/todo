from abc import ABC, abstractmethod

from pipe import SENTINEL
from utils.single_iter import single_iter

class Source(ABC):
    def __init__(self):
        self._children = []

    @abstractmethod
    def _produce(self):
        yield

    @single_iter(auto_start=False)
    def produce(self):
        yield from self._produce()

    def __rshift__(self, other):
        self._children.append(other)
        return other

    @staticmethod
    def _terminate(child):
        try:
            return child.send(SENTINEL)
        except StopIteration:
            return None

    def send_to_pipe(*senders):
        all_children = []

        for sender in senders:
            receivers = [child.consume() for child in sender._children]
            all_children += receivers

            sender = sender.produce()

            for item in sender:
                for child in receivers:
                    child.send(item)

        results = [
            result for result_list in (
                Source._terminate(child)
                for child in all_children
            ) if result_list is not None
            for result in result_list
        ]
        return results
