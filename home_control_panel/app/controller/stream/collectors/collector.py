import os
import json
import time
from enum import Enum
from imutils import grab_contours
from cv2 import (
    resize,
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
    return abs(int(hash(str(time) + str(address))))
