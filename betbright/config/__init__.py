import yaml

_yaml_path = 'betbright/config/local.yml'
with open(_yaml_path, 'r') as file:
    settings = yaml.load(file)
