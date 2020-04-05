# YAML files

## layers/[layer_name]/layer.yml

name: python
injections:
  vim_plug:
    Plug "test"

commands:
  pre-enable:
    - mv ~/test
  post-enable:
    - echo "Done"

## templates/[template_name]/template.yml

name: neovim
destination: $HOME/.config/neovim.vim

## templates/[template_name]/template.jinja2

Plug#start
{{ injections.vim_plug }}
Plug#end

# Command line

layer enable python
layer disable python
layer list
layer apply
layer 
  --enabled-layers-file=~/.config/layers4all/enabled 
  --templates-dir=~/.config/layers4all/templates 
  --layers-dir=~/.config/layers4all/layers 
  enable python

# Structure

/layers4all/model.py
  Config:
    layers_file
    templates_dir
    layers_dir

  Layer:
    name: str
    injections: Dict[str, str]
    pre_install_commands: []
    post_install_commands: []

  Context:
    injections: Dict[str, str]
    env: Dict[str,str] # Environment vars

  Template:
    name: str
    dest: str

/layers4all/template.py
  def load(dir) -> Template
  def render(ctx: Context, template: Template)

/layers4all/layer.py (layer reading, injection, etc)
  def load(dir) -> Layer
  def setup(layer)
  def post_setup(layer)
/layers4all/bin.py (entrypoint)
/layers4all/commands.py (enable / disable / list / reload)
