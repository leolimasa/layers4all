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
    injections: Dict[str, List[str]]
    pre_enable_commands: List[str]
    post_enable_commands: List[str]


@dataclass
class Template:
    name: str
    dest: str
    template: str
    pre_enable_commands: List[str]
    post_enable_commands: List[str]


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
    templates: List[Template]
