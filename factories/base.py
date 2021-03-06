import importlib
import os
from abc import ABC
from typing import Type

from utils import get_subclasses


class BaseFactory(ABC):
    """
    Discovers and registers subclasses of base_class in discovery_path
    in a factory.
    """
    registry: dict
    discovery_path: str
    base_class: Type

    def __init__(self):
        modules = list(map(
            lambda f: ".".join([self.discovery_path, f[:f.find(".py")]]),
            filter(lambda f: not f.startswith("__"), os.listdir(self.discovery_path))
        ))
        for module in modules:
            importlib.import_module(module)

        base_subclasses = get_subclasses(self.base_class)
        for subclass in base_subclasses:
            # Store the type. Lazily instantiate it when needed
            self.registry[subclass.name] = subclass

    def get_instance(self, key):
        if key not in self.registry:
            return None

        # Always instantiate the object and return it, no lazy
        return self.registry[key]()
