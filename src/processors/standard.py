from pipe import SENTINEL
from processors.formatter import Formatter

class StandardFormatter(Formatter):
    def _process(self):
        now = self._now()

        while True:
            item = yield
            if item is SENTINEL:
                break

            yield f"{item.summary} - {self._format_date(item.deadline, now)}"

        yield
