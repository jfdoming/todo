import json

from config.actions import get_action

class Step:
    def __init__(self, step):
        self.criteria = step.get("criteria", [])
        self.actions = list(map(get_action, step["actions"]))

class Config:
    def __init__(self, path):
        with open(path, "r") as f:
            config = json.loads(f.read())
        self.courses = set(config.get("courses", []))
        self.steps = (
            list(map(Step, config["steps"]))
            if "steps" in config
            else None
        )
