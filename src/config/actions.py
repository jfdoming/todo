from config.expansion import Expansion

class Action:
    pass

class FilterDeadlineAction(Action):
    def __init__(self, action):
        self.after = action["after"]


class ExpandAction(Action):
    def __init__(self, action):
        self.to = list(map(Expansion, action["to"]))

_ACTIONS = ("type", {
    "filter": ("target", {
        "deadline": FilterDeadlineAction,
    }),
    "expand": ExpandAction,
})

def get_action(action, lookup=None):
    if isinstance(lookup, type):
        return lookup(action)

    if lookup is None:
        lookup = _ACTIONS

    lookup_type, lookup_dict = lookup
    if lookup_type not in action:
        raise TypeError(
            f"Missing action attribute \"{lookup_type}\" in action {action}"
        )

    action_type = action[lookup_type]
    if action_type not in lookup_dict:
        raise TypeError(
            f"Invalid action type \"{action_type}\" "
            + f"for action attribute \"{lookup_type}\""
        )

    lookup = lookup_dict[action_type]
    return get_action(action, lookup)
