from argparse import ArgumentParser

from pipe.source import Source
from calendar_api import CalendarAPI
from models.event_list import EventList
from views.cli_view import CliView
from views.clipboard_view import ClipboardView
from processors.standard import StandardFormatter
from processors.shareable import ShareableFormatter
from processors.event_processor import EventProcessor
from collectors.todo_list_collector import TodoListCollector


def main():
    parser = ArgumentParser(
        prog="todo",
        description=(
            "Command-line TODO utility, integrated with Google Calendar."
        ),
    )
    parser.add_argument(
        "-s",
        "--shareable",
        dest="shareable",
        action="store_true",
    )
    args = parser.parse_args()

    api = CalendarAPI()
    cal_lists = EventList.from_user_calendars(api)

    # Convert all calendar events to Todo items.
    todo_collector = TodoListCollector()
    for cal_list in cal_lists:
        cal_list >> EventProcessor() >> todo_collector

    primary_list = Source.send_to_pipe(*cal_lists)[0]

    views = [CliView()]

    if args.shareable:
        formatter = ShareableFormatter()
        views.append(ClipboardView())
    else:
        formatter = StandardFormatter()

    primary_list >> formatter
    for view in views:
        formatter >> view

    primary_list.send_to_pipe()


if __name__ == "__main__":
    main()
