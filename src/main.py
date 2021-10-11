from argparse import ArgumentParser

from api import API
from calendar_todo_list import CalendarTodoList
from primary_todo_list import PrimaryTodoList
from cli_tl_view import CliTlView


def main():
    parser = ArgumentParser(prog="todo", description="Command-line TODO utility, integrated with Google Calendar.")
    parser.add_argument("-s", "--shareable", dest="shareable", action="store_true")
    args = parser.parse_args()

    api = API()
    cal_lists = CalendarTodoList.from_user_calendars(api)
    primary_list = PrimaryTodoList(cal_lists)

    view = CliTlView(primary_list, args)
    view.display()


if __name__ == "__main__":
    main()
