import pytz
from datetime import datetime, timedelta

class Expansion:
    def __init__(self, to):
        import dateparser # Lazy import.
        if isinstance(to, str):
            self.name = to
            self.deadline = timedelta(0)
            return

        self.name = to["name"]

        now = datetime.utcnow().replace(tzinfo=pytz.utc)
        self.deadline = dateparser.parse(
            to["deadline"],
            settings={
                "TIMEZONE": "UTC",
                "TO_TIMEZONE": "UTC",
                "RETURN_AS_TIMEZONE_AWARE": True,
                "RELATIVE_BASE": now,
            },
        )
        if "relative" not in to or to["relative"]:
            self.deadline = self.deadline - now

        self.keep_numbering = (to.get("numbering") == "keep")
