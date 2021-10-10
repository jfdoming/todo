from abc import ABC, abstractmethod

class TodoListView(ABC):
    def __init__(self, target):
        self.target = target

    @abstractmethod
    def display(self):
        pass
