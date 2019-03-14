import settings
from commands.base import BaseCommand


class Help(BaseCommand):
    name = "help"

    def help(self) -> str:
        return f"Usage: {settings.COMMAND_PREFIX}{self.name} <command>"

    def run(self, arg) -> str:
        if not arg:
            return self.help()
        from globals import command_factory
        command = command_factory.get_instance(arg)
        if command is None:
            return f"Command {arg} does not exist!"
        return command.help()
