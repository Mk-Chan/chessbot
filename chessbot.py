import settings
from communication_services.base import BaseCommunicationService
from globals import command_factory, communication_service_factory


def listener(service: BaseCommunicationService):
    while True:
        print("Listening!")
        text = service.recv()
        print(f"RECVD: {text}")
        if text.startswith(settings.COMMAND_PREFIX):
            space_index = text.find(" ")
            if space_index == -1:
                space_index = len(text) + 1
            command = text[len(settings.COMMAND_PREFIX):space_index]
            command_handler = command_factory.get_instance(command)
            if command_handler is None:
                continue
            command_args = text[space_index + 1:]
            response = command_handler.run(command_args)
            service.send(response)


if __name__ == "__main__":
    communication_service = communication_service_factory \
        .get_instance(settings.COMMUNICATION_SERVICE)
    listener(communication_service)
