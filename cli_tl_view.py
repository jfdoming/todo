import humanize
from datetime import datetime
import pytz

from todo_list_view import TodoListView

class CliTlView(TodoListView):
    def __format_date(self, date, now):
        return humanize.naturaltime(date, when=now)

    def display(self):
        now = datetime.utcnow().replace(tzinfo=pytz.utc)

        seen_any = False
        for item in self.target.list():
            seen_any = True
            print(f"{item.summary} - {self.__format_date(item.deadline, now)}")

        if not seen_any:
            print("No upcoming events found.")
