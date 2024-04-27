from pipe.standard import Filter

class DoneFilter(Filter):
    def __init__(self, done):
        super().__init__(self.__check_item(done))

    def __check_item(self, done):
        done = set(done)
        def __check(item):
            return f"{hash(item):0{16}x}" not in done
        return __check
