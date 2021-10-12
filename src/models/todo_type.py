from enum import Enum, unique

@unique
class TodoType(Enum):
    DEFAULT = ""
    ASSIGNMENT = "assignment"
    QUIZ = "quiz"
    TEST = "test"
    EXAM = "exam"

    # Thanks to https://stackoverflow.com/a/19300424.
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, human_name):
        self.human_name = human_name

    @classmethod
    def from_summary(cls, summary):
        parts = summary.split()

        if len(parts) < 3:
            return TodoType.DEFAULT
        if not parts[0].isalpha():
            return TodoType.DEFAULT
        if not parts[1].isdigit():
            return TodoType.DEFAULT
        parts = parts[2:]
        for part in parts:
            if part.lower() in TodoType.__NAME_TO_ENUM:
                return TodoType.__NAME_TO_ENUM[part.lower()]

TodoType._TodoType__NAME_TO_ENUM = {
    TodoType[member].human_name: TodoType[member]
    for member in TodoType.__members__
}
