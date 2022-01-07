import os
import sys
import pickle

_CONFIG_HOME = (os.environ.get("CONFIG_HOME") or os.path.dirname(sys.argv[0]))

def _config(name):
    return os.path.join(_CONFIG_HOME, name)

TOKEN_FILE = _config("token.json")
CREDENTIALS_FILE = _config("credentials.json")
CALENDARS_FILE = _config("calendars.json")

_CONFIG_FILE = _config("config.json")
_CONFIG_COMPILED = _CONFIG_FILE + ".pkl"
CONFIG = None
if os.path.exists(_CONFIG_COMPILED):
    from datetime import datetime
    with open(_CONFIG_COMPILED, "rb") as f:
        try:
            CONFIG = pickle.load(f)
        except:
            CONFIG = None
        if CONFIG is not None:
            stats = os.stat(_CONFIG_FILE)
            last = datetime.fromtimestamp(stats.st_mtime)
            if last > CONFIG.freshness:
                CONFIG = None
if CONFIG is None:
    from config.config import Config
    CONFIG = Config(_CONFIG_FILE)
    with open(_CONFIG_COMPILED, "wb") as f:
        pickle.dump(CONFIG, f)
