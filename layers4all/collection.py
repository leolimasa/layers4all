from . import template
from typing import Dict, List
from .model import Context, Layer, Collection
from functools import reduce


def injections(col: Collection) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {}
    for layer in col.enabled_layers:
        for k in layer.injections:
            if not k in result:
                result[k] = layer.injections[k]
            else:
                result[k] = result[k] + layer.injections[k]
    return result


def context(col: Collection) -> Context:
    return Context(injections=injections(col))
