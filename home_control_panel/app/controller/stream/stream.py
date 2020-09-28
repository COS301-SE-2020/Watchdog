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
    THRESH_BINARY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE,
    COLOR_BGR2GRAY,
    COLOR_BGR2RGB
)
from .collectors.video import FrameCollector
from .collectors.image import ImageCollector
from .collectors.collector import (
    Tag,
    time_now
)
from ....service.detection import FastMTCNN


device = 'cuda' if torch.cuda.is_available() else 'cpu'


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
        self.address = address
        self.stream_view = None
        self.stream_connection = None
        self.current_frame = None
        # Collectors
        self.image_collector = ImageCollector(self.camera_id, self.address)
        self.frame_collector = FrameCollector(self.camera_id, self.address)
        # Indicators for Analysis
        self.indicators = SimpleNamespace()
        self.indicators.ceil = 100.0
        self.indicators.weight = 0.3
        self.indicators.average = None
        self.indicators.fast_mtcnn = FastMTCNN(
            stride=4,
            min_confidence=90,
            resize=1,
            margin=14,
            factor=0.6,
            keep_all=True,
            device=device
        )
        # Trigger Checks
        self.triggers = SimpleNamespace()
        self.triggers.is_movement = False
        self.triggers.is_person = False
        self.triggers.movement_buffer = 1500
        self.triggers.movement_timer = time_now() + self.triggers.movement_buffer
        # Start Collectors
        self.image_collector.start()
        self.frame_collector.start()

    # Add frame to stream
    def put(self, frame):
        now = time_now()
        self.current_frame = resize(frame, (self.width, self.height))
        # Check if there was any Recent Movement
        if now <= self.triggers.movement_timer:
            # Detect Face in Current Frame
            if self.detect_person():
                self.frame_collector.collect(frame, Tag.DETECTED)
                self.image_collector.collect(frame)
            elif self.triggers.is_movement:
                self.frame_collector.collect(frame, Tag.MOVEMENT)
        else:
            self.frame_collector.collect(frame, Tag.PERIODIC)
            # Detect Movement in Current Frame
            if self.detect_movement():
                self.triggers.movement_timer = now + self.triggers.movement_buffer
        # Update UI Component
        if self.stream_view is not None:
            self.stream_view.update_frame(cvtColor(self.current_frame, COLOR_BGR2RGB))
        # Update Online Livestream
        if self.stream_connection is not None:
            self.stream_connection.produce(self.camera_id, self.current_frame)

    # Detects Persons Face in Frame
    def detect_person(self):
        self.triggers.is_person = self.indicators.fast_mtcnn(self.current_frame)
        return self.triggers.is_person

    # Detects Movement in Frame
    def detect_movement(self):
        if self.indicators.average is None:
            self.indicators.average = array(self.current_frame, float)
        # Update Moving Average
        accumulateWeighted(self.current_frame, self.indicators.average, self.indicators.weight)
        difference = cvtColor(absdiff(self.current_frame, convertScaleAbs(self.indicators.average)), COLOR_BGR2GRAY)
        thresh = erode(dilate(threshold(difference, 70, 255, THRESH_BINARY)[1], None, iterations=1), None, iterations=1)
        # Build Contours
        contours = grab_contours(findContours(thresh, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE))
        current_surface_area = 0.0
        for contour in contours:
            current_surface_area += contourArea(contour)
        # Set Trigger
        mult = 0.95
        self.triggers.is_movement = False
        if current_surface_area > self.indicators.ceil:
            mult = 1.05
            self.triggers.is_movement = True
        self.indicators.ceil = max(self.indicators.ceil * mult, 80.0)
        return self.triggers.is_movement

    # Set UI Stream View Component
    def set_view(self, view):
        self.stream_view = view

    # Remove UI Stream View Component
    def clear_view(self):
        self.stream_view = None

    # Resize Stream Dimensions
    def size(self, width, height):
        (self.width, self.height) = (int(width), int(height))
