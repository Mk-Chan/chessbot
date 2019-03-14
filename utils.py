import itertools
from typing import List, Type


def filtered_split(text: str) -> List[str]:
    return list(filter(None, text.split(" ")))


def get_subclasses(cls: Type) -> List[Type]:
    immediate_subclasses = cls.__subclasses__()
    return immediate_subclasses + list(
        itertools.chain(*[
            get_subclasses(subclass)
            for subclass in immediate_subclasses
        ])
    )
