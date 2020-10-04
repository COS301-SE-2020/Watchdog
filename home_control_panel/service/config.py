import os
import json


def setup():
    print('Setting up Paths...')
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data/temp'):
        os.mkdir('data/temp')
    if not os.path.exists('data/temp/video'):
        os.mkdir('data/temp/video')
    if not os.path.exists('data/temp/image'):
        os.mkdir('data/temp/image')


setup()

default_path = 'data/.conf'

print('CONFIG LOADING...')

if not os.path.exists(default_path):
    default_settings = {
        "settings": {
            "site": "My Household",
            "address": "My Address",
            "live": True,
            "recording_ratio": "1.0"
        },
        "services": {
            "connect": True,
            "stream_url": "https://stream.watchdog.thematthew.me:443/",
            "base_url": "https://b534kvo5c6.execute-api.af-south-1.amazonaws.com",
            "client": {
                "id": "5bl2caob065vqodmm3sobp3k7d",
                "pool": "eu-west-1_mQ0D78123",
                "key": "supersecure"
            }
        },
        "video": {
            "resolution": {
                "width": 360,
                "height": 200
            },
            "clip_length": 60.0,
            "frames_per_second": 7
        },
        "image": {
            "capture_limit": 7.0,
            "image_threshold": 1
        }
    }

    with open(default_path, 'w') as file:
        json.dump(default_settings, file, indent=4)


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
