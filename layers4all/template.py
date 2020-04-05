import os
import yaml
from .common import render_template_str, parse_commands, read_file, write_file, run_command
from .model import Template, Context


def from_yaml(yaml_str: str, template: str) -> Template:
    parsed = yaml.load(yaml_str)
    return Template(
        name=parsed['name'],
        dest=render_template_str(parsed['destination']),
        template=template,
        pre_enable_commands=parse_commands(
            parsed.get('commands', {}).get('pre-enable', [])),
        post_enable_commands=parse_commands(
            parsed.get('commands', {}).get('post-enable', []))
    )


def from_dir(dir_path: str) -> Template:
    template_yaml_path = os.path.join(dir_path, "template_config.yaml")
    template_jinja_path = os.path.join(dir_path, "template.jinja")
    template_yaml = read_file(template_yaml_path)
    template_jinja = read_file(template_jinja_path)
    return from_yaml(template_yaml, template_jinja)


def render(ctx: Context, template: Template) -> str:
    return render_template_str(
        template.template,
        {"injections": ctx.injections}
    )


def save(ctx: Context, template: Template) -> None:
    rendered = render(ctx, template)
    write_file(template.dest, rendered)


def run_pre_commands(template: Template) -> None:
    for c in template.pre_enable_commands:
        run_command(c)


def run_post_commands(template: Template) -> None:
    for c in template.post_enable_commands:
        run_command(c)
