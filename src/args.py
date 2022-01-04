from argparse import ArgumentParser as _Parser
from datetime import timedelta as _delta

def parse_args():
    parser = _Parser(
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

    def offset(x):
        return _delta(int(x))
    parser.add_argument(
        "-b",
        "--back",
        "--offset",
        dest="offset",
        type=offset,
    )

    args = parser.parse_args()
    return args

