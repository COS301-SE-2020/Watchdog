import json
import threading
import time
from enum import Enum
from cv2 import (
    VideoWriter,
    VideoWriter_fourcc,
    resize
)


fps = 15
clip_length = 60
recording_ratio = 0.5


# 1 = periodically saved frames (user defined length & frequency)
# 2 = live intruder alert capture frame (a face is present in the scene)
class Tag(Enum):
    DEFAULT = 0
    PERIODIC = 1
    ACTIVITY = 2
    ALERT = 3


class Video:
    def __init__(self, address, tag=Tag.DEFAULT):
        self.frames = []
        self.tag = tag
        self.time_start = time_now()
        self.time_end = time_now()
        self.address = address
        self.id = hash_id(self.time_start, self.address)

    def resize(self, width, height):
        for index in range(len(self.frames)):
            resize(self.frames[index], (width, height))

    def add_frame(self, frame):
        if frame is not None:
            self.frames.append(frame)
        self.time_end = time_now()

    def set_frames(self, frames):
        for index in range(len(frames)):
            self.add_frame(frames[index])
        self.time_end = time_now()

    def export(self):
        if len(self.frames) > 0:
            name = 'data/temp/video/' + self.id + '.mp4'
            (h, w) = self.frames[0].shape[:2]
            file = VideoWriter(name, VideoWriter_fourcc(*'mp4v'), fps, (w, h), True)
            print("Exporting Video [" + name + "]")
            for index in range(len(self.frames)):
                if self.frames[index] is not None:
                    file.write(self.frames[index])
            file.release()

    def get_metadata(self):
        meta_data = {
            "clip_id": self.id,
            "time_start": str(self.time_start)[0:19],
            "time_end": str(self.time_end)[0:19],
            "address": self.address,
            "tag": self.tag
        }
        return json.dumps(meta_data)


#################################################
# FrameCollector
#   Maintains a frame queue
#   Exports Frames as Images
#   Exports videos
#################################################
# Video Management Procedure:
#   If current frame has face
#       Add frame to f_queue
#   Else
#       Add None to f_queue
#   If current frame has movement
#       Add frame to m_queue
#   Else
#       Add None to m_queue
#   Add frame to p_queue
#################################################
# Video AssemBly Procedure:
#   1. Create Empty Frame Queue of Same Length
#       i. This queue cannot be filled over a specified % in any of the following procedures
#   2. Fill new queue with f_queue frames
#   3. Fill new queue with m_queue frames
#   4. Fill new queue with p_queue frames
#   5. Export Video, ignoring emptry frames
#################################################
# Queue Flushing Procedure
#   Queues are flushed every 1 minute
#       Fetch user Period Recording Config
#           Record a specified % of the minute
#           Prioritise which queue frames are consolidated into the clip for that minute
#               Priorities: Face -> Movement -> None
#   When Flushing Frame Collector
#       Consolidate different queues into clips
#           Ensure no duplicates are stored
#       Using the queues (of equal length, sometimes containing empty frames) build a clip of %minute length
#################################################
class FrameCollector(threading.Thread):
    def __init__(self, address):
        threading.Thread.__init__(self)
        self.alert_queue = []
        self.move_queue = []
        self.period_queue = []
        self.address = address
        self.live = False

    def run(self):
        self.live = True
        while(self.live):
            progress = len(self.period_queue) / (fps * clip_length)
            if progress >= 1.0:
                self.flush()
            else:
                time.sleep(clip_length * (1.0 - progress))

    def collect(self, frame, tag=Tag.DEFAULT):
        if tag == Tag.ALERT:
            self.alert_queue.append(frame)
        else:
            self.alert_queue.append(None)

        if tag == Tag.ACTIVITY:
            self.move_queue.append(frame)
        else:
            self.move_queue.append(None)

        self.period_queue.append(frame)

    def flush(self):
        tag = Tag.DEFAULT
        frame_count = 0
        cons_queue = []

        max_frames = recording_ratio * len(self.period_queue)
        for index in range(len(self.period_queue)):
            cons_queue.append(None)

        for index in range(len(self.alert_queue)):
            if frame_count > max_frames:
                break
            if self.alert_queue[index] is not None:
                cons_queue[index] = self.alert_queue[index]
                frame_count += 1
                tag = Tag.ALERT

        for index in range(len(self.move_queue)):
            if frame_count > max_frames:
                break
            if cons_queue[index] is None and self.move_queue[index] is not None:
                cons_queue[index] = self.move_queue[index]
                frame_count += 1
                if tag == Tag.DEFAULT:
                    tag = Tag.ACTIVITY

        for index in range(int(len(self.period_queue) / 2)):
            if frame_count > max_frames:
                break
            if cons_queue[index] is None and self.period_queue[index] is not None:
                cons_queue[index] = self.period_queue[index]
                frame_count += 1
                if tag == Tag.DEFAULT:
                    tag = Tag.PERIODIC
            alt_index = len(self.period_queue) - index - 1
            if cons_queue[alt_index] is None and self.period_queue[alt_index] is not None:
                cons_queue[alt_index] = self.period_queue[alt_index]
                frame_count += 1
                if tag == Tag.DEFAULT:
                    tag = Tag.PERIODIC

        # while frame_count > max_frames:
        #     index += randint(1, int(len(self.period_queue) / 10))
        #     if cons_queue[index] is None and self.period_queue[index] is not None:
        #         for step in range(fps / 2):
        #             cons_queue[index - step] = self.period_queue[index - step]
        #         for step in range(fps / 2):
        #             cons_queue[index + step] = self.period_queue[index + step]
        #         # cons_queue[index] = self.period_queue[index]
        #         frame_count += 1
        #         tag = Tag.PERIODIC
        #     if index >= len(self.period_queue):
        #         index = 0

        videoxx = Video('xxxx', tag)
        videoxx.set_frames(self.period_queue)
        videoxx.export()

        self.alert_queue.clear()
        self.move_queue.clear()
        self.period_queue.clear()

        video = Video(self.address, tag)
        video.set_frames(cons_queue)
        video.export()

        return video

# Determines if two frames are distinct from one another
#   Use Pixels, Location, Time, etc...
def distinct_frames(frame_x, frame_y):
    return False


def time_now():
    return int(round(time.time() * 1000))  # milliseconds

def hash_id(time, address=''):
    return str(time) + str(hash(address))