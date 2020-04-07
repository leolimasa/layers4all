import os
import yaml
from .common import render_template_str, parse_commands, read_file, write_file, run_command, FieldMissing, require_fields
from .model import TemplateConfig, Context, Template
from typing import Dict, List


def make_template(dir_path: str,
                  template_yaml: Dict[str, str]) -> Template:
    require_fields(['destination', 'file'], template_yaml)
    return Template(
        dest=os.path.expandvars(
            os.path.expanduser(template_yaml['destination'])),
        template_str=read_file(
            os.path.join(dir_path, template_yaml['file']))
    )


def from_yaml(yaml_str: str, dir_path: str) -> TemplateConfig:
    parsed = yaml.load(yaml_str, Loader=yaml.FullLoader)
    required_fields = ['name', 'templates']

    return TemplateConfig(
        name=parsed['name'],
        dir_name=os.path.basename(dir_path),
        templates=[make_template(dir_path, t) for t in parsed['templates']],
        pre_save_commands=parse_commands(
            parsed.get('commands', {}).get('pre-save', [])),
        post_save_commands=parse_commands(
            parsed.get('commands', {}).get('post-save', []))
    )


class TemplateConfigYamlFieldMissing(Exception):
    def __init__(self, yaml_path: str, field_name: str):
        self.yaml_path = yaml_path
        self.field_name = field_name


def from_dir(dir_path: str) -> TemplateConfig:
    template_yaml_path = os.path.join(dir_path, "template_config.yaml")
    template_yaml = read_file(template_yaml_path)
    try:
        return from_yaml(template_yaml, dir_path)
    except FieldMissing as e:
        raise TemplateConfigYamlFieldMissing(template_yaml_path, e.field_name)


def render(ctx: Context, template: Template) -> str:
    return render_template_str(
        template.template_str,
        {"injections": ctx.injections}
    )


def save(ctx: Context, templatecfg: TemplateConfig) -> None:
    for t in templatecfg.templates:
        rendered = render(ctx, t)
        write_file(t.dest, rendered)


def run_pre_commands(template: TemplateConfig) -> None:
    for c in template.pre_save_commands:
        run_command(c)


def run_post_commands(template: TemplateConfig) -> None:
    for c in template.post_save_commands:
        run_command(c)
