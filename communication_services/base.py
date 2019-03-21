from abc import ABC, abstractmethod


class BaseCommunicationService(ABC):
    name: str

    @abstractmethod
    def send(self, text) -> None:
        pass

    @abstractmethod
    def recv(self) -> str:
        pass

    @abstractmethod
    def is_active(self) -> bool:
        return False
