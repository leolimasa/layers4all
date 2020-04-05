import argparse
import os
from . import commands, config
from .model import Config


def main() -> None:
    parser = make_parser()
    args = parser.parse_args()
    action = args.action
    cfg = Config(
        enabled_layers_file=args.enabled_layers_file,
        templates_dir=args.templates_dir,
        layers_dir=args.layers_dir
    )

    if action == "list":
        do_list(cfg)
    elif action == "enable":
        commands.enable(cfg, args.layer)
    elif action == "disable":
        commands.disable(cfg, args.layer)
    elif action == "apply":
        commands.apply(cfg)
    else:
        parser.print_help()


def do_list(cfg: Config) -> None:
    collection = config.collection(cfg)
    enabled_layers = [l.name for l in collection.enabled_layers]
    available_layers = [l.name for l in collection.available_layers]

    for l in sorted(available_layers):
        checkmark = "✔" if l in enabled_layers else " "
        print(checkmark + " " + l)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Manages system-wide configuration layers.'
    )
    subparsers = parser.add_subparsers(help='sub command help')

    list_sub = subparsers.add_parser('list')
    list_sub.add_argument(action='store_const', dest='action', const='list')

    list_sub = subparsers.add_parser('apply')
    list_sub.add_argument(action='store_const', dest='action', const='apply')

    enable_sub = subparsers.add_parser('enable')
    enable_sub.add_argument('layer', help='Layer name to enable')
    enable_sub.add_argument(action='store_const', dest='action', const='enable')

    disable_sub = subparsers.add_parser('disable')
    disable_sub.add_argument('layer', help='Layer name to disable')
    disable_sub.add_argument(action='store_const', dest='action', const='disable')

    parser.add_argument(
        '--enabled-layers-file',
        dest='enabled_layers_file',
        default=os.getenv(
            'L4A_ENABLED_LAYERS_FILE',
            os.path.expanduser('~/.config/layers4all/enabled_layers')
        ),
        help="Path to the file that stores which layers have been enabled. Defaults to env L4A_ENABLED_LAYERS_FILE or ~/.config/layers4all/enabled_layers."
    )
    parser.add_argument(
        '--templates-dir',
        dest='templates_dir',
        default=os.getenv(
            'L4A_TEMPLATES_DIR',
            os.path.expanduser('~/.config/layers4all/templates')
        ),
        help="Path to the directory containing templates definitions. Defaults to env L4A_TEMPLATES_DIR or ~/.config/layers4all/templates."
    )
    parser.add_argument(
        '--layers-dir',
        dest='layers_dir',
        default=os.getenv(
            'L4A_LAYERS_DIR',
            os.path.expanduser('~/.config/layers4all/layers')
        ),
        help="Path to the directory containing layer definitions. Defaults to env L4A_TEMPLATES_DIR or ~/.config/layers4all/layers."
    )
    return parser


if __name__ == '__main__':
    main()