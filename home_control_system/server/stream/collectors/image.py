import json
import copy
import threading
import time
from enum import Enum
from imutils import grab_contours
from cv2 import (
    resize,
    imwrite,
    absdiff,
    cvtColor,
    dilate,
    erode,
    threshold,
    contourArea,
    THRESH_BINARY,
    findContours,
    COLOR_BGR2GRAY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE
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

    def collect(self, frame):
        self.queue.append(frame)

    def sort(self):
        for index in range(len(self.queue)):
            for step in range(len(self.queue)):
                if index < len(self.queue) and step < len(self.queue) and not distinct_frames(self.queue[index], self.queue[step]):
                    del self.queue[step]

    def flush(self):
        self.sort()
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
    (width, height) = (30, 30)
    difference = cvtColor(absdiff(
        resize(
            frame_x,
            (width, height)
        ),
        resize(
            frame_y,
            (width, height)
        )
    ), COLOR_BGR2GRAY)
    thresh = erode(
        dilate(
            threshold(difference, 70, 255, THRESH_BINARY)[1],
            None,
            iterations=2
        ), None, iterations=1
    )
    contours = grab_contours(
        findContours(
            thresh,
            RETR_EXTERNAL,
            CHAIN_APPROX_SIMPLE
        )
    )
    current_surface_area = 0.0
    for contour in contours:
        current_surface_area += contourArea(contour)
    return current_surface_area > 1000.0

def time_now():
    return int(round(time.time() * 1000))  # milliseconds

def hash_id(time, address=''):
    return str(time) + str(hash(address))
