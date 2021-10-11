import os.path

from pick import pick
import json
from datetime import datetime, timedelta

from todo_list import TodoList
from todo_item import TodoItem

class CalendarTodoList(TodoList):
    def __init__(self, api, cid):
        self.api = api
        self.cid = cid

    @classmethod
    def from_user_calendars(cls, api):
        try:
            with open("calendars.json", "r") as calendars:
                selected_calendars = json.loads(calendars.read())
        except:
            pass

        if selected_calendars is None:
            calendars = api.list_calendars()
            selected_calendars = map(lambda c: c[0][0], pick(
                calendars,
                "Please mark your TODO calendars (SPACE to mark, ENTER to confirm):",
                multiselect=True,
                min_selection_count=1,
                options_map_func=lambda t: t[1],
            ))

            with open("calendars.json", "w") as calendars:
                calendars.write(json.dumps(selected_calendars))

        return list(map(
            lambda c: CalendarTodoList(api, c),
            selected_calendars,
        ))

    def list(self):
        start = datetime.utcnow()
        end = start + timedelta(days=14)

        events = self.api.get_upcoming_events(
            cid=self.cid,
            start=start,
            end=end,
        )
        for i in range(len(events)):
            event = events[i]
            events[i] = TodoItem(event.summary, event.start)

        return events

