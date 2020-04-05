from . import config, collection, template, layer
from .common import write_file
from .model import Layer, Template, Config
from typing import List
from enum import Enum
from dataclasses import dataclass


class EnableStatus(Enum):
    SUCCESS = 1
    ALREADY_ENABLED = 2


def enable(cfg: Config, layer_name: str) -> EnableStatus:
    enabled = [l.name for l in config.enabled_layers(cfg)]
    if layer_name in enabled:
        return EnableStatus.ALREADY_ENABLED
    write_file(cfg.enabled_layers_file, "\n".join(enabled + [layer_name]))
    return EnableStatus.SUCCESS


class DisableStatus(Enum):
    SUCCESS = 1
    ALREADY_DISABLED = 2


def disable(cfg: Config, layer_name: str) -> DisableStatus:
    enabled = [l.name for l in config.enabled_layers(cfg)]
    if layer_name not in enabled:
        return DisableStatus.ALREADY_DISABLED
    enabled.remove(layer_name)
    write_file(cfg.enabled_layers_file, "\n".join(enabled))
    return DisableStatus.SUCCESS


def apply(cfg: Config) -> None:
    col = config.collection(cfg)
    ctx = collection.context(col)

    for t in col.templates:
        template.run_pre_commands(t)

    for l in col.enabled_layers:
        layer.run_pre_commands(l)

    for t in col.templates:
        template.save(ctx, t)

    for l in col.enabled_layers:
        layer.run_post_commands(l)

    for t in col.templates:
        template.run_post_commands(t)
