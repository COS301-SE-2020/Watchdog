import json
import time
import cv2 as cv
from enum import Enum

# 1 = periodically saved frames (user defined length & frequency)
# 2 = live intruder alert capture frame (a face is present in the scene)
class Tag(Enum):
    DEFAULT = 0
    PERIODIC = 1
    ALERT = 2


class Frame:
    def __init__(self, frame, address, tag=Tag.DEFAULT):
        self.frame = frame
        self.tag = tag
        self.time = time_now()
        self.address = address
        self.id = hash_id(self.time, self.address)

    def resize(self, width, height):
        cv.resize(self.frame, (width, height))

    def export(self):
        return cv.imwrite("data/temp/image/%s.jpg" % self.id, self.frame)

    def get_metadata(self):
        meta_data = {
            "frame_id": self.id,
            "timestamp": str(self.time)[0:19],
            "address": self.address,
            "tag": self.tag
        }
        return json.dumps(meta_data)


def time_now():
    return int(round(time.time() * 1000))  # milliseconds

def hash_id(time, address):
    return str(time) + str(hash(address))
