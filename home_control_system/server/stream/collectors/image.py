import json
import copy
import threading
import time
from enum import Enum
from cv2 import (
    resize,
    imwrite
)


# 1 = periodically saved frames (user defined length & frequency)
# 2 = live intruder alert capture frame (a face is present in the scene)
class Tag(Enum):
    DEFAULT = 0
    PERIODIC = 1
    ACTIVITY = 2
    ALERT = 3


class Image:
    def __init__(self, frame, address, tag=Tag.DEFAULT):
        self.frame = frame
        self.tag = tag
        self.time = time_now()
        self.address = address
        self.id = hash_id(self.time, self.address)

    def reframe(self, width, height):
        resize(self.frame, (width, height))

    def export(self):
        return imwrite("data/temp/image/%s.jpg" % self.id, self.frame)

    def get_metadata(self):
        meta_data = {
            "frame_id": self.id,
            "timestamp": str(self.time)[0:19],
            "address": self.address,
            "tag": self.tag
        }
        return json.dumps(meta_data)


class ImageCollector(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.queue = []
        self.live = False
        self.address = address

    def run(self):
        self.live = True
        while(self.live):
            time.sleep(5)
            self.flush()

#   def sort(self):
#         unique = True
#         for index in range(len(self.queue)):
#             if not distinct_frames(self.queue[index], frame):
#                 unique = False

    def collect(self, frame):
        self.queue.append(frame)

    def flush(self):
        if len(self.queue) == 0:
            return None
        images = []
        for index in range(len(self.queue)):
            image = Image(
                self.queue[index],
                self.address,
                Tag.ALERT
            )
            images.append(image)
            image.export()
        self.queue.clear()
        return images

    def retrieve_images(self, drop=False):
        if drop:
            image_list = copy.deepcopy(self.images)
            self.images.clear()
            return image_list
        return self.images

# Determines if two frames are distinct from one another
#   Use Pixels, Location, Time, etc...
def distinct_frames(frame_x, frame_y):
    return False

def time_now():
    return int(round(time.time() * 1000))  # milliseconds

def hash_id(time, address=''):
    return str(time) + str(hash(address))