import os
import json


def configure():
    with open('data/settings.conf') as config_file:
        data = json.load(config_file)
        os.environ['config'] = json.dumps(data)


configure()