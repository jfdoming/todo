from argparse import ArgumentParser

from pipe.source import Source
from calendar_api import CalendarAPI
from models.event_list import EventList
from views.cli_view import CliView
from views.clipboard_view import ClipboardView
from processors.standard import StandardFormatter
from processors.shareable import ShareableFormatter
from processors.event_processor import EventProcessor
from processors.done_filter import DoneFilter
from collectors.todo_list_collector import TodoListCollector
from collectors.done_collector import DoneCollector


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
    parser.add_argument(
        "-d",
        "--done",
        dest="done",
        action="append",
        default=[],
    )
    args = parser.parse_args()

    api = CalendarAPI()
    cal_lists = EventList.from_user_calendars(api)

    # Convert all calendar events to Todo items, filtering out items being
    # marked as done.
    done_filter = DoneFilter(args.done)
    for cal_list in cal_lists:
        cal_list >> EventProcessor() >> done_filter
    done_filter >> TodoListCollector()

    # Explicit (non-member) invocation in order to collect all events in
    # parallel. Indexed to retrieve the first result.
    primary_list = Source.send_to_pipe(cal_lists)

    primary_list >> DoneCollector(api)

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
