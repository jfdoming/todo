from todo_list_view import TodoListView

class CliTlView(TodoListView):
    __ASSESSMENT_SHORT_FORMS = {
        "assignment": "a",
        "quiz": "q",
        "test": "exam ",
    }

    def __init__(self, children, args):
        super().__init__(children)
        self.shareable = args.shareable

        if self.shareable:
            self.item_format = "- {0}"
        else:
            self.item_format = "{0} - {1}"

    def __short_format(self, summary):
        parts = summary.split()
        if not parts:
            return summary
        if not parts[0].isupper() or not parts[0].isalpha():
            return summary

        del parts[0]
        parts[1] = parts[1].lower()
        if (
            parts[1] in CliTlView.__ASSESSMENT_SHORT_FORMS
            and len(parts) == 3
            and parts[2].isdigit()
        ):
            parts[1] = CliTlView.__ASSESSMENT_SHORT_FORMS[parts[1]] + parts[2]
            del parts[2]

        return " ".join(parts)

    def display(self):
        now = self._now()

        seen_any = False
        for item in self.target.list():
            seen_any = True
            summary = item.summary
            deadline = self._format_date(item.deadline, now)
            if self.shareable:
                summary = self.__short_format(summary)
            print(self.item_format.format(summary, deadline))

        if not seen_any:
            print("No upcoming events found.")
