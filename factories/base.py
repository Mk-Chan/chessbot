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
        lazy_instance = self.registry[key]

        # If type has been instantiated, return the object
        if isinstance(lazy_instance, self.base_class):
            return lazy_instance

        # Otherwise, instantiate the object and return it
        instance = self.registry[key] = lazy_instance(*lazy_instance.init_params)
        return instance
