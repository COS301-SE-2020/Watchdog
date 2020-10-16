import json
import copy
import threading
import time
from cv2 import (
    imwrite,
    resize
)
from .collector import (
    Tag,
    time_now,
    hash_id,
    capture_limit,
    image_threshold
)
from .....service import services


class ImageCollector(threading.Thread):
    def __init__(self, camera_id, address):
        threading.Thread.__init__(self)
        self.camera_id = camera_id
        self.address = address
        self.queue = []
        self.live = False

    def run(self):
        self.live = True
        while(self.live):
            self.flush()
            time.sleep(1)

    def collect(self, frame):
        self.queue.append(frame)

    def flush(self):
        if len(self.queue) == 0:
            return None
        count = 0
        images = []
        start = time_now()
        for index in range(len(self.queue)):
            image = Image(
                self.camera_id,
                self.queue[index],
                self.address,
                Tag.DETECTED
            )
            images.append(image)
            image.export()
            diff = time_now() - start
            time.sleep(max(capture_limit - diff, 0.0))

            count += 1
            if count > image_threshold:
                break
        self.queue.clear()
        self.queue = []
        return images

    def retrieve_images(self, drop=False):
        if drop:
            image_list = copy.deepcopy(self.images)
            self.images.clear()
            return image_list
        return self.images


class Image:
    def __init__(self, camera_id, frame, address, tag=Tag.DEFAULT):
        self.camera_id = camera_id
        self.frame = frame
        self.tag = tag
        self.time = time_now()
        self.address = address
        self.id = hash_id(self.time, self.address)

    def reframe(self, width, height):
        resize(self.frame, (width, height))

    def export(self):
        if self.tag == Tag.DEFAULT:
            return

        imwrite("data/temp/image/%s.jpg" % str(self.id), self.frame)

        if self.tag == Tag.DETECTED:
            tag_label = 'detected'
        elif self.tag == Tag.INTRUDER:
            tag_label = 'intruder'

        services.upload_to_s3('data/temp/image', str(self.id) + '.jpg', tag_label, self.camera_id)
        return True

    def get_metadata(self):
        meta_data = {
            "frame_id": self.id,
            "timestamp": str(self.time)[0:19],
            "address": self.address,
            "tag": self.tag
        }
        return json.dumps(meta_data)
