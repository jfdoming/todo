from args import parse_args
from pipe.source import Source
from calendar_api import CalendarAPI
from models.event_list import EventList
from views.cli_view import CliView
from views.clipboard_view import ClipboardView
from processors.standard import StandardFormatter
from processors.shareable import ShareableFormatter
from processors.event_processor import EventProcessor
from collectors.todo_list_collector import TodoListCollector
from collectors.done_collector import DoneCollector

def main():
    args = parse_args()

    api = CalendarAPI()
    cal_lists = EventList.from_user_calendars(api, offset=args.offset)

    # Convert all calendar events to Todo items.
    todo_collector = TodoListCollector()
    for cal_list in cal_lists:
        cal_list >> EventProcessor() >> todo_collector

    # Explicit (non-member) invocation in order to collect all events in
    # parallel. Indexed to retrieve the first result.
    primary_list = Source.send_to_pipe(*cal_lists)[0]

    primary_list >> DoneCollector(api, args.done)

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
