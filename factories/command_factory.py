from commands.base import BaseCommand
from factories.base import BaseFactory


class CommandFactory(BaseFactory):
    registry = {}
    discovery_path = 'commands'
    base_class = BaseCommand
