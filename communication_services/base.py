from abc import ABC, abstractmethod
from typing import List


class BaseCommunicationService(ABC):
    name: str
    init_params: List = []

    @abstractmethod
    def send(self, text) -> None:
        pass

    @abstractmethod
    def recv(self) -> str:
        pass
