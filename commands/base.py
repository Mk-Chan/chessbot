from abc import ABC, abstractmethod
from typing import List


class BaseCommand(ABC):
    name: str
    init_params: List = []

    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def run(self, arg) -> str:
        pass
