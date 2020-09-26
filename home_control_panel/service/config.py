import os
import json


default_path = 'data/.conf'


def configure(path=default_path):
    with open(path) as config_file:
        data = json.load(config_file)
        os.environ['config'] = json.dumps(data)
    return json.loads(os.environ['config'])


def update_config(key, value, path=default_path):
    conf = json.loads(os.environ['config'])
    conf[key] = value
    with open(path, 'w') as config_file:
        json.dump(conf, config_file, indent=4)


try:
    configure()
except Exception:
    pass
