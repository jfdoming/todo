from functools import wraps

class __PollableGenerator:
    def __run(self, gen):
        try:
            val = yield next(gen)
            while True:
                val = yield gen.send(val)
        except StopIteration:
            self.done = True

    def __init__(self, gen):
        self.done = False
        self.gen = self.__run(gen)

def single_iter(fn=None, auto_start=True):
    def annotation(fn):
        @wraps(fn)
        def run(self, *args, **kwargs):
            name = f"_memo_{fn.__name__}"
            has_next = False
            if hasattr(self, name):
                gen = getattr(self, name)
                has_next = not gen.done
            if not has_next:
                gen = __PollableGenerator(fn(self, *args, **kwargs))
                if auto_start:
                    next(gen.gen)
                setattr(self, name, gen)
            return getattr(self, name).gen
        return run

    if fn is not None:
        return annotation(fn)
    return annotation
