import subprocess

from pipe.source import SENTINEL
from pipe.sink import Sink

class ClipboardView(Sink):
    def consume(self):
        data = ""

        while True:
            item = yield
            if item is SENTINEL:
                break
            data += item + "\n"

        p = subprocess.Popen(
            ["xclip", "-selection", "c"],
            stdin=subprocess.PIPE,
            close_fds=True,
        )
        p.communicate(input=data.encode("utf-8"))

        yield