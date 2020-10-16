import os
import time
import json
import threading
import imageio
from cv2 import (
    resize,
    imwrite
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

        try:
            for filename in os.listdir('./data/temp/frame'):
                os.remove(filename)
        except Exception:
            pass

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
        max_frames = recording_ratio * len(self.period_queue)

        video = Video(self.camera_id, self.address, Tag.DEFAULT)

        for index in range(len(self.period_queue)):
            if index > max_frames:
                break
            if self.alert_queue[index] is not None:
                video.tag = Tag.INTRUDER
                video.add_frame(self.alert_queue[index])
            elif self.move_queue[index] is not None:
                video.add_frame(self.move_queue[index])
                video.tag = Tag.MOVEMENT
            elif self.period_queue[index] is not None:
                video.add_frame(self.period_queue[index])
                video.tag = Tag.PERIODIC

        video.export()

        self.clear()
        return video

    def clear(self):
        self.alert_queue = []
        self.move_queue = []
        self.period_queue = []

class Video:
    def __init__(self, camera_id, address, tag=Tag.DEFAULT):
        self.camera_id = camera_id
        self.address = address
        self.tag = tag
        self.dimensions = (RES_X, RES_Y)
        self.time_start = time_now()
        self.time_end = time_now()
        self.frames = []
        self.id = hash_id(self.time_start, self.address)

    def add_frame(self, frame):
        if frame is not None:
            frame_name = 'data/temp/frame/{}.jpg'.format(str(self.id) + str(len(self.frames)))
            self.frames.append(frame_name)
            imwrite(frame_name, frame)
        self.time_end = time_now()

    def set_frames(self, frames):
        for index in range(len(frames)):
            self.add_frame(frames[index])
        self.time_end = time_now()

    def export(self):
        if self.tag != Tag.DEFAULT and len(self.frames) > 0:
            ext = '.mp4'
            name = ('./data/temp/video/{}' + ext).format(str(self.id))

            print("Exporting Video [" + name + "]")
            writer = imageio.get_writer(name, fps=fps, macro_block_size=0)
            for index in range(len(self.frames)):
                if self.frames[index] is not None:
                    writer.append_data(imageio.imread(self.frames[index]))
                    os.remove(self.frames[index])
            writer.close()

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
