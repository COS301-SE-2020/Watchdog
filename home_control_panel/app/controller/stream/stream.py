import torch
from numpy import array
from imutils import grab_contours
from types import SimpleNamespace
from cv2 import (
    accumulateWeighted,
    findContours,
    contourArea,
    convertScaleAbs,
    cvtColor,
    threshold,
    dilate,
    erode,
    absdiff,
    resize,
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE
)
from .collectors.video import FrameCollector
from .collectors.image import ImageCollector
from .collectors.collector import (
    Tag,
    time_now
)
from ....service.face_detection import FastMTCNN

# Stream
#   In-Out Frame Processing Pipe
#      Does Movement Detection & Face Detection
#      Periodically Stacks frames then Exports Result Video
#      Handles Intruder Alert Frames then Adds to ImageCollector which Exports the Result Image
#   Upload the Result Videos and Images to S3 Bucket
class Stream:
    def __init__(self, camera_id, address, dimensions):
        self.size(dimensions[0], dimensions[1])
        self.camera_id = camera_id
        self.current_frame = None
        self.address = address
        self.stream_connection = None
        # Checks
        self.triggers = SimpleNamespace()
        self.triggers.is_movement = False
        self.triggers.is_person = False
        self.triggers.movement_buffer = 1500
        self.triggers.movement_timer = time_now() + self.triggers.movement_buffer
        # Indicators for Analysis
        self.indicators = SimpleNamespace()
        self.indicators.ceil = 100.0
        self.indicators.weight = 0.3
        self.indicators.average = None
        # Collectors
        self.image_collector = ImageCollector(self.address)
        self.frame_collector = FrameCollector(self.address)
        self.frame_collector.camera_id = self.camera_id
        self.image_collector.camera_id = self.camera_id
        self.image_collector.start()
        self.frame_collector.start()

        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.fast_mtcnn = FastMTCNN(
            stride=4,
            min_confidence=90,
            resize=1,
            margin=14,
            factor=0.6,
            keep_all=True,
            device=device
        )

    # Add frame to stream
    def put(self, frame):
        now = time_now()
        self.current_frame = resize(frame, (self.width, self.height))

        self.triggers.is_person = False
        # Check if there was any Recent Movement
        if now <= self.triggers.movement_timer:
            # Detect Face in Current Frame
            if self.detect_person():
                self.triggers.is_person = True
                self.frame_collector.collect(frame, Tag.DETECTED)
                self.image_collector.collect(frame)
            elif self.detect_movement:
                self.frame_collector.collect(frame, Tag.MOVEMENT)
        else:
            self.frame_collector.collect(frame, Tag.PERIODIC)
            # Detect Movement in Current Frame
            if self.detect_movement():
                self.triggers.is_movement = True
                self.triggers.movement_timer = now + self.triggers.movement_buffer
            else:
                self.triggers.is_movement = False

        if self.stream_connection is not None:
            self.stream_connection.produce(self.camera_id, self.current_frame)

    # Detects Movement in Frame
    #   Returns True if Movement
    #   Fills Feedback Buffer for Movement
    def detect_movement(self):
        if self.indicators.average is None:
            self.indicators.average = array(self.current_frame, float)
            
        accumulateWeighted(
            self.current_frame,
            self.indicators.average,
            self.indicators.weight
        )

        difference = cvtColor(
            absdiff(
                self.current_frame,
                convertScaleAbs(self.indicators.average)
            ), COLOR_BGR2GRAY
        )

        thresh = erode(
            dilate(
                threshold(difference, 70, 255, THRESH_BINARY)[1],
                None,
                iterations=1
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

        if current_surface_area > self.indicators.ceil:
            self.indicators.ceil *= 1.05
            return True
        self.indicators.ceil *= 0.95
        self.indicators.ceil = max(self.indicators.ceil, 100.0)
        return False

    # Detects Persons Face in Frame
    #   Returns True if Face Present
    #   Fills Feedback Buffer for Faces
    def detect_person(self):
        return self.fast_mtcnn(self.current_frame)

    def size(self, width, height):
        (self.width, self.height) = (int(width), int(height))
