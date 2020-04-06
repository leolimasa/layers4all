import os
import yaml
from .common import render_template_str, parse_commands, read_file, write_file, run_command
from .model import Template, Context


class YamlFieldMissing(Exception):
    def __init__(self, field: str):
        self.field_name = field


def from_yaml(yaml_str: str, template: str, dir_name: str) -> Template:
    parsed = yaml.load(yaml_str, Loader=yaml.FullLoader)
    required_fields = ['name', 'destination']
    for f in required_fields:
        if f not in parsed:
            raise YamlFieldMissing(f)

    return Template(
        name=parsed['name'],
        dir_name=dir_name,
        dest=os.path.expanduser(render_template_str(parsed['destination'])),
        template=template,
        pre_save_commands=parse_commands(
            parsed.get('commands', {}).get('pre-save', [])),
        post_save_commands=parse_commands(
            parsed.get('commands', {}).get('post-save', []))
    )


class TemplateYamlFieldMissing(Exception):
    def __init__(self, yaml_path: str , field_name: str):
        self.yaml_path = yaml_path 
        self.field_name = field_name


def from_dir(dir_path: str) -> Template:
    template_yaml_path = os.path.join(dir_path, "template_config.yaml")
    template_jinja_path = os.path.join(dir_path, "template.jinja")
    template_yaml = read_file(template_yaml_path)
    template_jinja = read_file(template_jinja_path)
    try:
        return from_yaml(template_yaml, template_jinja, os.path.basename(dir_path))
    except YamlFieldMissing as e:
        raise TemplateYamlFieldMissing(template_yaml_path, e.field_name)


def render(ctx: Context, template: Template) -> str:
    return render_template_str(
        template.template,
        {"injections": ctx.injections}
    )


def save(ctx: Context, template: Template) -> None:
    rendered = render(ctx, template)
    write_file(template.dest, rendered)


def run_pre_commands(template: Template) -> None:
    for c in template.pre_save_commands:
        run_command(c)


def run_post_commands(template: Template) -> None:
    for c in template.post_save_commands:
        run_command(c)
