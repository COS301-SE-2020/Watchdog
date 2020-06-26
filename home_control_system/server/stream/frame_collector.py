import copy
import threading
import time
from .frame import (
    Frame,
    Tag,
    time_now
)


# FrameCollector
#   Maintains a frame queue
#       Ensures that each Collected Frame is Distinct from All Other Frames in Queue
#   Exports Frames as Images
class FrameCollector(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.queue = {}
        self.images = {}

    def run(self):
        while(True):
            self.flush()
            time.sleep(10)

    def collect(self, frame, address):
        frame = Frame(
            frame,
            address,
            Tag.ALERT
        )
        unique = True
        for frame_name, queue_frame in self.queue.items():
            if not distinct_frames(queue_frame, frame):
                unique = False
        if unique:
            self.queue[frame.id] = frame

    def flush(self):
        for frame_name, queue_frame in self.queue.items():
            queue_frame.export()
        self.queue.clear()

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
