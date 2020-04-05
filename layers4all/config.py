import os

from . import layer
from . import template
from .common import read_file, list_dirs, list_dirs, create_file_if_not_exists
from .model import Config, Layer, Template, Collection
from typing import List


def enabled_layers(config: Config) -> List[Layer]:
    create_file_if_not_exists(config.enabled_layers_file)
    enabled_layers_str = read_file(config.enabled_layers_file)
    if enabled_layers_str == '':
        return []
    enabled_layers = [l.strip() for l in enabled_layers_str.split("\n")]
    return [
        layer.from_dir(os.path.join(config.layers_dir, l))
        for l in enabled_layers
    ]


def templates(config: Config) -> List[Template]:
    template_dirs = list_dirs(config.templates_dir)
    return [template.from_dir(d) for d in template_dirs]


def collection(cfg: Config) -> Collection:
    return Collection(
        enabled_layers=enabled_layers(cfg),
        available_layers=layer.available_layers(cfg.layers_dir),
        templates=templates(cfg)
    )
