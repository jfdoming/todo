from argparse import ArgumentParser

from calendar_api import CalendarAPI
from models.calendar_todo_list import CalendarTodoList
from models.primary_todo_list import PrimaryTodoList
from views.cli_view import CliView
from views.clipboard_view import ClipboardView
from processors.standard import StandardFormatter
from processors.shareable import ShareableFormatter


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
    cal_lists = CalendarTodoList.from_user_calendars(api)
    primary_list = PrimaryTodoList(cal_lists)

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
