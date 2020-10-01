import os
import time
import json
import threading
from cv2 import (
    VideoWriter,
    VideoWriter_fourcc,
    resize
)
from .collector import (
    Tag,
    time_now,
    hash_id,
    fps,
    clip_length,
    recording_ratio
)
from .....service import services

conf = json.loads(os.environ['config'])
FPS = conf['video']['frames_per_second']
(RES_X, RES_Y) = (conf['video']['resolution']['width'], conf['video']['resolution']['height'])

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
    def __init__(self, camera_id, address):
        threading.Thread.__init__(self)
        self.dimensions = (RES_X, RES_Y)
        self.camera_id = camera_id
        self.address = address
        self.alert_queue = []
        self.move_queue = []
        self.period_queue = []
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
        (width, height) = self.dimensions
        frame = resize(frame, (width, height))
        if tag == Tag.INTRUDER:
            self.alert_queue.append(frame)
        else:
            self.alert_queue.append(None)

        if tag == Tag.MOVEMENT:
            self.move_queue.append(frame)
        else:
            self.move_queue.append(None)

        self.period_queue.append(frame)

    def flush(self):
        tag = Tag.DEFAULT
        cons_queue = []
        frame_count = 0
        max_frames = recording_ratio * len(self.period_queue)

        # Build Empty Frame Queue
        for index in range(len(self.period_queue)):
            cons_queue.append(None)

        # Fill Queue with Frames Containg Faces
        for index in range(len(self.alert_queue)):
            if frame_count > max_frames:
                break
            if self.alert_queue[index] is not None:
                tag = Tag.INTRUDER
                if index > 0:
                    cons_queue[index - 1] = self.period_queue[index - 1]
                    frame_count += 1
                cons_queue[index] = self.alert_queue[index]
                frame_count += 1
                if index < len(self.period_queue) - 2:
                    cons_queue[index + 1] = self.period_queue[index + 1]
                    frame_count += 1

        # Fill Queue with Frames Containg Movement
        for index in range(len(self.move_queue)):
            if frame_count > max_frames:
                break
            if cons_queue[index] is None and self.move_queue[index] is not None:
                cons_queue[index] = self.move_queue[index]
                frame_count += 1
                if tag == Tag.DEFAULT:
                    tag = Tag.MOVEMENT

        # Fill Queue with Remaining Frames until Full
        #   Filling is performed moving towards the centre, from the four quarter locations in the queue
        size = int(len(self.period_queue) / 4)
        for index in range(size):
            if frame_count > max_frames:
                break
            if cons_queue[index] is None and self.period_queue[index] is not None:
                cons_queue[index] = self.period_queue[index]
                frame_count += 1
            if cons_queue[index + size] is None and self.period_queue[index + size] is not None:
                cons_queue[index + size] = self.period_queue[index + size]
                frame_count += 1
            alt_index = len(self.period_queue) - index - 1
            if cons_queue[alt_index - size] is None and self.period_queue[alt_index - size] is not None:
                cons_queue[alt_index - size] = self.period_queue[alt_index - size]
                frame_count += 1
            if cons_queue[alt_index] is None and self.period_queue[alt_index] is not None:
                cons_queue[alt_index] = self.period_queue[alt_index]
                frame_count += 1
            if tag == Tag.DEFAULT:
                tag = Tag.PERIODIC

        video = Video(self.camera_id, self.address, tag)
        video.set_frames(cons_queue)
        video.export()

        self.alert_queue.clear()
        self.move_queue.clear()
        self.period_queue.clear()
        self.alert_queue = []
        self.move_queue = []
        self.period_queue = []
        return video


class Video:
    def __init__(self, camera_id, address, tag=Tag.DEFAULT):
        self.camera_id = camera_id
        self.frames = []
        self.tag = tag
        self.time_start = time_now()
        self.time_end = time_now()
        self.address = address
        self.dimensions = (RES_X, RES_Y)
        self.id = hash_id(self.time_start, self.address)

    def resize(self, dimensions):
        self.dimensions = (width, height) = dimensions
        for index in range(len(self.frames)):
            self.frames[index] = resize(self.frames[index], (width, height))

    def add_frame(self, frame):
        if frame is not None:
            self.frames.append(frame)
        self.time_end = time_now()

    def set_frames(self, frames):
        for index in range(len(frames)):
            self.add_frame(frames[index])
        self.time_end = time_now()

    def export(self):
        if self.tag == Tag.DEFAULT:
            return
        if len(self.frames) > 0:
            ext = '.mp4'
            name = 'data/temp/video/' + str(self.id) + ext
            (width, height) = self.dimensions
            (w, h) = (width, height)
            self.resize((w, h))

            file = VideoWriter(name, VideoWriter_fourcc(*'mp4v'), fps, (w, h), True)

            print("Exporting Video [" + name + "]")
            for index in range(len(self.frames)):
                if self.frames[index] is not None:
                    file.write(self.frames[index])
            file.release()

            if self.tag == Tag.PERIODIC:
                tag_label = 'periodic'
            elif self.tag == Tag.MOVEMENT:
                tag_label = 'movement'
            elif self.tag == Tag.DETECTED:
                tag_label = 'detected'
            elif self.tag == Tag.INTRUDER:
                tag_label = 'intruder'

            services.upload_to_s3('data/temp/video', str(self.id) + ext, tag_label, self.camera_id)

            return True

        return False

    def get_metadata(self):
        meta_data = {
            "clip_id": self.id,
            "time_start": str(self.time_start)[0:19],
            "time_end": str(self.time_end)[0:19],
            "address": self.address,
            "tag": self.tag
        }
        return json.dumps(meta_data)
