from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

import os.path
from datetime import datetime, timedelta
import iso8601
import pytz

from event import Event

class API:
    __SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

    def __init__(self):
        self.service = self.__get_service()

    def __get_service(self):
        creds = None
        # The file token.json stores the user"s access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", API.__SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", API.__SCOPES)
                creds = flow.run_console()
            # Save the credentials for the next run
            with open("token.json", "w") as token:
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
            events[i] = Event(start=start, summary=event["summary"])

        return events
