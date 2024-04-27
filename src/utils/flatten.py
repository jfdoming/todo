# Thanks to https://stackoverflow.com/a/2158532.

from collections.abc import Iterable, Mapping

def flatten(l, max_depth=None):
    for el in l:
        if (
            (max_depth is None or max_depth > 0)
            and isinstance(el, Iterable)
            and not isinstance(el, (str, bytes, Mapping))
        ):
            yield from flatten(el)
        else:
            yield el
