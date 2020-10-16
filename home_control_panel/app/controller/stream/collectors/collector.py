import os
import json
import time
from enum import Enum


conf = json.loads(os.environ['config'])
fps = conf['video']['frames_per_second']
clip_length = conf['video']['clip_length']
recording_ratio = float(conf['settings']['recording_ratio'])
capture_limit = conf['image']['capture_limit']
image_threshold = conf['image']['image_threshold']


# 1 = periodically saved frames (user defined length & frequency)
# 2 = live intruder alert capture frame (a face is present in the scene)
class Tag(Enum):
    DEFAULT = 0
    PERIODIC = 1
    MOVEMENT = 2
    DETECTED = 3
    INTRUDER = 4


def time_now():
    return int(round(time.time() * 1000))  # milliseconds


def hash_id(time, address=''):
    return abs(int(hash(str(time) + str(address))))
