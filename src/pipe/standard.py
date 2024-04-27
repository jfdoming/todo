from pipe import SENTINEL, SKIP
from pipe.processor import Processor

class Filter(Processor):
    def __init__(self, fn):
        super().__init__()
        self.fn = fn

    def _process(self):
        while True:
            item = yield
            if item is SENTINEL:
                break
            if self.fn(item):
                print(item)
                yield item
            else:
                yield SKIP
