import os
import sys

from config.config import Config as _Config

_CONFIG_HOME = (
    os.environ.get("CONFIG_HOME")
    or os.path.join(os.path.dirname(sys.argv[0]), "config")
)

def _config(name):
    return os.path.join(_CONFIG_HOME, name)

TOKEN_FILE = _config("token.json")
CREDENTIALS_FILE = _config("credentials.json")
CALENDARS_FILE = _config("calendars.json")

CONFIG = _Config(_config("config.json"))
