from abc import ABC, abstractmethod

from pipe import SENTINEL, SKIP
from utils.single_iter import single_iter
from utils.flatten import flatten

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

    def __lshift__(self, other):
        other._children.append(self)
        return self

    @staticmethod
    def _terminate(child):
        try:
            return child.send(SENTINEL)
        except StopIteration:
            return None

    def __get_results(self, children):
        return flatten(filter(lambda c: c is not None, children), max_depth=1)

    def send_to_pipe(*senders, first_result=True):
        senders = map(lambda s: (s, s.produce()), flatten(senders))
        return self._send_to_pipe(senders, first_result=first_result)


    def _send_to_pipe(self, senders, first_result=False):
        all_children = []

        for sender, sender_it in senders:
            receivers = [child.consume() for child in sender._children]
            all_children += receivers

            for item in sender_it:
                if item is not SKIP:
                    for child in receivers:
                        child.send(item)

        results = [
            result for result_list in (
                Source._terminate(child)
                for child in all_children
            ) if result_list is not None and not print("result_list:", result_list)
            for result in result_list
        ]
        print(results)
        return (
            (results[0] if len(results) else None)
            if first_result
            else results
        )
