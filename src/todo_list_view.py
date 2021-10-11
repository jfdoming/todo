from datetime import datetime
import humanize
import pytz


from abc import ABC, abstractmethod

class TodoListView(ABC):
    def __init__(self, target):
        self.target = target

    def _now(self):
        return datetime.utcnow().replace(tzinfo=pytz.utc)

    def _format_date(self, date, now):
        return humanize.naturaltime(date, when=now)

    @abstractmethod
    def display(self):
        pass
