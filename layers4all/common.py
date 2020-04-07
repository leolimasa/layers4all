from typing import Dict, List, Any, Union
import jinja2 as jj
import os

ValidParam = Union[Dict[str, List[str]], str]


def render_template_str(template: str, params: Dict[str, ValidParam] = {}) -> str:
    tpl = jj.Template(template)
    return tpl.render(env=os.environ, **params)


def render_template_arr(templates: List[str], params: Dict[str, ValidParam] = {}) -> List[str]:
    return [render_template_str(t, params) for t in templates]


def read_file(path: str) -> str:
    text_file = open(path, "r")
    contents = text_file.read()
    text_file.close()
    return contents


def write_file(path: str, contents: str) -> None:
    f = open(path, "w")
    f.write(contents)
    f.close()


def parse_command(cmd: str) -> str:
    expanded = os.path.expanduser(os.path.expandvars(cmd))
    return render_template_str(expanded)


def parse_commands(cmds: List[str]) -> List[str]:
    return [parse_command(c) for c in cmds]


def run_command(cmd: str) -> None:
    os.system(cmd)


def dir_names_in_dir(dir_path: str) -> List[str]:
    if not os.path.exists(dir_path):
        return []
    return [o for o in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, o))]


def list_dirs(dir_path: str) -> List[str]:
    if not os.path.exists(dir_path):
        return []
    return [os.path.join(dir_path, o) for o in os.listdir(dir_path)
            if os.path.isdir(os.path.join(dir_path, o))]

def create_file_if_not_exists(file_path: str) -> None:
    dirname = os.path.dirname(file_path)
    if not os.path.exists(dirname):
        os.makedirs(os.path.dirname(file_path))
    if not os.path.exists(file_path):
        f = open(file_path, "w")
        f.close()

class FieldMissing(Exception):
    def __init__(self, field: str):
        self.field_name = field

def require_fields(fields: List[str], parsed: Dict[str, Any]) -> None:
    for f in fields:
        if f not in parsed:
            raise FieldMissing(f)
