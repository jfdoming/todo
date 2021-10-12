from argparse import ArgumentParser

from api import API
from calendar_todo_list import CalendarTodoList
from primary_todo_list import PrimaryTodoList
from cli_tl_view import CliTlView
from clipboard_view import ClipboardView
from process.standard import StandardFormatter
from process.shareable import ShareableFormatter


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

    api = API()
    cal_lists = CalendarTodoList.from_user_calendars(api)
    primary_list = PrimaryTodoList(cal_lists)

    views = [CliTlView()]

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
