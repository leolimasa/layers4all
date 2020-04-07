import os
import yaml
from .common import render_template_str, parse_commands, read_file, write_file, run_command, list_dirs, create_file_if_not_exists
from .model import Layer
from typing import List


def from_yaml(yaml_str: str, dir_name: str) -> Layer:
    parsed = yaml.load(yaml_str, Loader=yaml.FullLoader)
    injections = parsed['injections'] if 'injections' in parsed else {}

    return Layer(
        name=parsed['name'],
        dir_name=dir_name,
        injections=injections,
        pre_template_commands=parse_commands(
            parsed.get('commands', {}).get('pre-template', [])),
        post_template_commands=parse_commands(
            parsed.get('commands', {}).get('post-template', []))
    )


def from_dir(dir_path: str) -> Layer:
    yaml_path = os.path.join(dir_path, 'layer_config.yaml')
    return from_yaml(read_file(yaml_path), os.path.basename(dir_path))


def available_layers(layers_dir: str) -> List[Layer]:
    layer_dirs = list_dirs(layers_dir)
    return [
        from_dir(d)
        for d in layer_dirs
        if os.path.exists(os.path.join(d, 'layer_config.yaml'))
    ]


def new(layers_dir: str, layer_name: str) -> None:
    file_path = os.path.join(layers_dir, layer_name, 'layer_config.yaml')
    create_file_if_not_exists(file_path)
    write_file(file_path, f"name: {layer_name}\ninjections:")


def export_env(layers_dir: str, layer: Layer) -> None:
    layer_path = os.path.join(layers_dir, layer.dir_name)
    os.environ['LAYER_DIR'] = layer_path


def run_pre_commands(layers_dir: str, layer: Layer) -> None:
    export_env(layers_dir, layer)
    for c in layer.pre_template_commands:
        run_command(c)


def run_post_commands(layers_dir: str, layer: Layer) -> None:
    export_env(layers_dir, layer)
    for c in layer.post_template_commands:
        run_command(c)
