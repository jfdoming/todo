from datetime import datetime
import humanize
import pytz

from pipe.processor import Processor

class Formatter(Processor):
    def _now(self):
        return datetime.utcnow().replace(tzinfo=pytz.utc)

    def _format_date(self, date, now):
        return humanize.naturaltime(date, when=now)
