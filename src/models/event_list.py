import sys
import os.path

from pick import pick
import json
from datetime import datetime, timedelta

from config import CALENDARS_FILE
from pipe.source import Source
from models.todo_item import TodoItem

class EventList(Source):
    def __init__(self, api, cid, offset=None):
        super().__init__()

        self.api = api
        self.cid = cid
        self.offset = offset

    @classmethod
    def from_user_calendars(cls, api, offset=None):
        try:
            with open(CALENDARS_FILE, "r") as calendars:
                selected_calendars = json.loads(calendars.read())
        except:
            selected_calendars = None

        if selected_calendars is None:
            calendars = api.get_calendars()
            selected_calendars = list(map(lambda c: c[0][0], pick(
                calendars,
                "Please mark your TODO calendars (SPACE to mark, ENTER to confirm):",
                multiselect=True,
                min_selection_count=1,
                options_map_func=lambda t: t[1],
            )))

            with open("calendars.json", "w") as calendars:
                calendars.write(json.dumps(selected_calendars))

        return list(map(
            lambda c: EventList(api, c, offset=offset),
            selected_calendars,
        ))

    def _produce(self):
        offset = self.offset
        start = datetime.utcnow()
        if offset is not None:
            start += offset
        end = start + timedelta(days=14)

        events = self.api.get_upcoming_events(
            cid=self.cid,
            start=start,
            end=end,
        )

        yield from iter(events)
