import os

from . import layer
from . import template
from .common import read_file, dir_names_in_dir
from .model import Config, Layer, Template
from typing import List


def enabled_layers(config: Config) -> List[Layer]:
    enabled_layers_str = read_file(config.enabled_layers_file)
    enabled_layers = [l.strip() for l in enabled_layers_str.split("\n")]
    return [
        layer.from_dir(os.path.join(config.layers_dir, l))
        for l in enabled_layers
    ]

def templates(config: Config) -> List[Template]:
    template_dirs = dir_names_in_dir(config.templates_dir)
    return [template.from_dir(d) for d in template_dirs]

