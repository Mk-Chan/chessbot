from communication_services.base import BaseCommunicationService


class CommandLineService(BaseCommunicationService):
    name = "cmdline"

    def send(self, text) -> None:
        print(f"SENDING: {text}")

    def recv(self) -> str:
        return input("Enter Text: ")
