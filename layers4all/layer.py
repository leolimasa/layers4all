import os
import yaml
from .common import render_template_str, parse_commands, read_file, write_file, run_command
from .model import Layer
from typing import List

def from_yaml(yaml_str: str) -> Layer:
    parsed = yaml.load(yaml_str)  
    return Layer(
          name = parsed['name'],
          injections = parsed['injections'],
          pre_enable_commands = parse_commands(
              parsed.get('commands', {}).get('pre-enable',[])),
          post_enable_commands = parse_commands(
              parsed.get('commands', {}).get('post-enable', []))
          )

def from_dir(dir_path: str) -> Layer:
    yaml_path = os.path.join(dir_path, 'layer_config.yaml')
    return from_yaml(read_file(yaml_path))

def run_pre_commands(layer: Layer) -> None:
    for c in layer.pre_enable_commands:
        run_command(c)

def run_post_commands(layer: Layer) -> None:
    for c in layer.post_enable_commands:
        run_command(c)
