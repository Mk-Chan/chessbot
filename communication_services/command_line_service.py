from communication_services.base import BaseCommunicationService


class CommandLineService(BaseCommunicationService):
    name = "cmdline"

    def send(self, text) -> None:
        print(f"SEND:{text}")

    def recv(self) -> str:
        text = input("Enter Text: ")
        print(f"RECV:{text}")
        return text

    def is_active(self) -> bool:
        return True
