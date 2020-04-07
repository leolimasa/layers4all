from dataclasses import dataclass
from typing import Dict, List

import jinja2 as jj


@dataclass
class Config:
    '''
    Overall configuration for the app.
    '''
    enabled_layers_file: str
    templates_dir: str
    layers_dir: str


@dataclass
class Layer:
    name: str
    dir_name: str
    injections: Dict[str, List[str]]
    pre_template_commands: List[str]
    post_template_commands: List[str]

@dataclass
class Template:
    dest: str
    template_str: str

@dataclass
class TemplateConfig:
    name: str
    dir_name: str
    templates: List[Template]
    pre_save_commands: List[str]
    post_save_commands: List[str]


@dataclass
class Context:
    '''
    Context that is sent to Templates so
    that they have enough information to render
    '''
    injections: Dict[str, List[str]]


@dataclass
class Collection:
    '''
    A collection of enabled templates and layers
    '''
    available_layers: List[Layer]
    enabled_layers: List[Layer]
    templates: List[TemplateConfig]
