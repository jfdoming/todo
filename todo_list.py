from abc import ABC, abstractmethod

class TodoList(ABC):
    @abstractmethod
    def list(self):
        pass
