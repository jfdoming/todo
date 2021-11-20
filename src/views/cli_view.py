from pipe import SENTINEL
from pipe.sink import Sink

class CliView(Sink):
    def _consume(self):
        seen_any = False
        while (item := (yield)) != SENTINEL:
            seen_any = True
            print(item)

        if not seen_any:
            print("No upcoming events found.")

        yield
