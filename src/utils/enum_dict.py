def enum_dict(cls):
    cls._NAME_TO_ENUM = {
        cls[member].human_name: cls[member]
        for member in cls.__members__
    }
    return cls
