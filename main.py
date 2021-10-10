from api import API
from todo import CalendarTodoList
from primary_todo_list import PrimaryTodoList
from cli_tl_view import CliTlView


def main():
    api = API()
    cal_lists = CalendarTodoList.from_user_calendars(api)
    primary_list = PrimaryTodoList(cal_lists)

    view = CliTlView(primary_list)
    view.display()


if __name__ == "__main__":
    main()
