import os
import yaml

_ENVINRONMENT = os.environ.get('ENV', 'local')
_yaml_path = 'betbright/config/{0}.yml'.format(_ENVINRONMENT)

with open(_yaml_path, 'r') as file:
    settings = yaml.load(file)
