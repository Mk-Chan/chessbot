from abc import ABC, abstractmethod


class BaseCommand(ABC):
    name: str

    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def run(self, arg) -> str:
        pass
