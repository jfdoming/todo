from pipe.source import SENTINEL
from process.formatter import Formatter

class ShareableFormatter(Formatter):
    __ASSESSMENT_SHORT_FORMS = {
        "assignment": "a",
        "quiz": "q",
        "test": "exam ",
    }

    def __short_format(self, summary):
        parts = summary.split()
        if not parts:
            return summary
        if not parts[0].isupper() or not parts[0].isalpha():
            return summary

        del parts[0]
        parts[1] = parts[1].lower()
        if (
            parts[1] in ShareableFormatter.__ASSESSMENT_SHORT_FORMS
            and len(parts) == 3
            and parts[2].isdigit()
        ):
            parts[1] = ShareableFormatter.__ASSESSMENT_SHORT_FORMS[parts[1]] + parts[2]
            del parts[2]

        return " ".join(parts)

    def process(self):
        while True:
            item = yield
            if item is SENTINEL:
                break

            yield f"- {self.__short_format(item.summary)}"

        yield
