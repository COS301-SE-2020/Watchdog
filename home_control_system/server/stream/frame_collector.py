import copy
from .frame import (
    Frame,
    Tag,
    time_now
)


# FrameCollector
#   Maintains a frame queue
#       Ensures that each Collected Frame is Distinct from All Other Frames in Queue
#   Exports Frames as Images
class FrameCollector:
    def __init__(self):
        self.queue = {}
        self.images = {}
        self.cooldown = time_now()

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
        if time_now() < self.cooldown:
            return False
        for frame_name, queue_frame in self.queue.items():
            queue_frame.export()
        self.queue.clear()
        self.cooldown = time_now() + 300000  # 5 minutes (milliseconds)
        return True

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
