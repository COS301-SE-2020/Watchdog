import os
import json


def configure():
    with open('data/settings.conf') as config_file:
        data = json.load(config_file)
        os.environ['config'] = json.dumps(data)
    return json.loads(os.environ['config'])

def update_config(key, value):
    conf = json.loads(os.environ['config'])
    conf[key] = value
    with open('data/settings.conf', 'w') as config_file:
        json.dump(conf, config_file)


configure()
