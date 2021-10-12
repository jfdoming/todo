from pipe.source import SENTINEL
from views.todo_list_view import TodoListView

class CliView(TodoListView):
    def consume(self):
        seen_any = False
        while (item := (yield)) != SENTINEL:
            seen_any = True
            print(item)

        if not seen_any:
            print("No upcoming events found.")

        yield
