from pipe.source import SENTINEL
from process.formatter import Formatter

class StandardFormatter(Formatter):
    def process(self):
        now = self._now()

        while True:
            item = yield
            if item is SENTINEL:
                break

            yield f"{item.summary} - {self._format_date(item.deadline, now)}"

        yield
