import os
from . import layer
from . import Template
from .model import Collection, Config, Context
from .common import read_file, dir_names_in_dir

def from_config(config: Config) -> Collection:
    enabled_layers_str = read_file(config.enabled_layers_file)
    enabled_layers = [l.strip() for l in enabled_layers_str.split("\n")]
    templates = dir_names_in_dir(config.templates_dir)
    


