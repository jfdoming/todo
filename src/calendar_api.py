from googleapiclient.discovery import build

import os.path
from datetime import datetime, timedelta
import iso8601
import pytz
import json
import re

from config import TOKEN_FILE, CREDENTIALS_FILE
from models.event import Event

_DESC_FMT = ">>>>>TODO<<<<<\n{}\n>>>END TODO<<<"
_DESC_REGEX = re.compile(_DESC_FMT.format("(.*)"), re.MULTILINE)

class CalendarAPI:
    __SCOPES = ["https://www.googleapis.com/auth/calendar"]

    def __init__(self):
        self.service = self.__get_service()

    def __get_service(self):
        creds = None
        # The file token.json stores the user"s access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(TOKEN_FILE):
            from google.oauth2.credentials import Credentials
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                CalendarAPI.__SCOPES,
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            create_new_token = True
            if creds and creds.expired and creds.refresh_token:
                try:
                    from google.auth.transport.requests import Request
                    creds.refresh(Request())
                    create_new_token = False
                except:
                    pass

            if create_new_token:
                from google_auth_oauthlib.flow import InstalledAppFlow
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE,
                    CalendarAPI.__SCOPES,
                )
                creds = flow.run_console()
            # Save the credentials for the next run
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build("calendar", "v3", credentials=creds)

    def __format_date(self, date):
        return date.isoformat() + "Z"

    def get_calendars(self):
        response = self.service.calendarList().list().execute()
        if not response:
            raise ValueError("Failed to list user calendars")
        items = response.get("items", [])
        if not items:
            raise ValueError("No user calendars!")
        calendars = [(entry["id"], entry["summary"]) for entry in items]
        return calendars

    def get_upcoming_events(self, cid, start=None, end=None):
        now = datetime.utcnow()

        if start is None:
            start = now
        if end is None:
            end = now + timedelta(days=1)

        start = self.__format_date(start)
        end = self.__format_date(end)

        events_result = self.service.events().list(
            calendarId=cid,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])

        for i in range(len(events)):
            event = events[i]
            start_obj = event.get("start")
            if not start_obj:
                continue
            if "dateTime" in start_obj and "timeZone" in start_obj:
                start_str = start_obj.get("dateTime")
                tz_str = start_obj.get("timeZone")
                start = iso8601.parse_date(start_str)
                start.replace(tzinfo=pytz.timezone(tz_str))
            elif "date" in start_obj:
                start = iso8601.parse_date(start_obj["date"])
            else:
                continue

            desc_raw = event.get("description")
            status = Event.STATUS_TODO
            if desc_raw is not None and desc_raw:
                desc = _DESC_REGEX.findall(desc_raw)
                if desc:
                    metadata = json.loads(desc[0])
                    status = metadata.get("status", Event.STATUS_TODO)
            events[i] = Event(
                raw=event,
                calendar_id=cid,
                start=start,
                summary=event["summary"],
                description=desc_raw,
                status=status,
            )

        return events

    def batch_mark_done(self, events):
        exceptions = []
        def _callback(rid, response, exception):
            if exception is not None:
                exceptions.append(exception)

        metadata = json.dumps({
            "status": Event.STATUS_DONE,
        })

        batch = self.service.new_batch_http_request(_callback)
        for event in events:
            body = event.raw
            description = "" if event.description is None else event.description
            desc = _DESC_REGEX.findall(description)
            if desc:
                description = _DESC_REGEX.sub(
                    _DESC_FMT.format(metadata) + "\n",
                    description
                )
            else:
                if description:
                    description += "\n"
                description += _DESC_FMT.format(metadata)
            body.update({
                "description": description,
            })

            batch.add(self.service.events().update(
                calendarId=event.cid,
                eventId=event.raw.get("id"),
                body=body,
            ))

        batch.execute()

        if exceptions:
            print(exceptions)
