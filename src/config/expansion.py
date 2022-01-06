from datetime import datetime, timedelta
import pytz
import parsedatetime

_DEADLINE_CAL = parsedatetime.Calendar()

class Expansion:
    def __init__(self, to):
        if isinstance(to, str):
            self.name = to
            self.deadline = timedelta(0)
            return

        self.name = to["name"]

        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        self.deadline, rc = _DEADLINE_CAL.parseDT(
            to["deadline"],
            sourceTime=now,
            tzinfo=pytz.utc,
        )
        if not rc:
            raise TypeError("Failed to parse deadline string")
        if "relative" not in to or to["relative"]:
            self.deadline = self.deadline - now

        self.keep_numbering = (to.get("numbering") == "keep")
