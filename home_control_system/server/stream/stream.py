from numpy import array
from imutils import grab_contours
from types import SimpleNamespace
from cv2 import (
    CascadeClassifier,
    drawContours,
    accumulateWeighted,
    findContours,
    contourArea,
    convertScaleAbs,
    cvtColor,
    threshold,
    dilate,
    erode,
    rectangle,
    absdiff,
    resize,
    data,
    COLOR_BGR2GRAY,
    THRESH_BINARY,
    RETR_EXTERNAL,
    CHAIN_APPROX_SIMPLE
)
from .collectors.image import (
    ImageCollector,
    Tag,
    time_now
)
from .collectors.video import FrameCollector


# Stream
#   In-Out Frame Processing Pipe
#      Does Movement Detection & Face Detection
#      Periodically Stacks frames then Exports Result Video
#      Handles Intruder Alert Frames then Adds to ImageCollector which Exports the Result Image
#   Upload the Result Videos and Images to S3 Bucket
class Stream:
    def __init__(self, address, dimensions):
        self.size(dimensions[0], dimensions[1])
        self.current_frame = None
        self.address = address
        self.stack = []
        # Stream View
        self.stream_views = []
        # Config for Periodic Video
        self.config = SimpleNamespace()
        self.config.frames_per_second = 30.0  # seconds
        self.config.clip_length = 10000  # milliseconds
        self.config.gap_length = 20000  # milliseconds
        self.config.start_time = time_now()
        self.config.stop_time = time_now() + self.config.clip_length
        # Feedback to be Outputted to Frame
        self.feedback = SimpleNamespace()
        self.feedback.contours = None
        self.feedback.faces = None
        self.feedback.irides = None
        self.feedback.bodies = None
        # Checks
        self.triggers = SimpleNamespace()
        self.triggers.is_movement = False
        self.triggers.is_person = False
        self.triggers.movement_timer = time_now() + 1500
        # Indicators for Analysis
        self.indicators = SimpleNamespace()
        self.indicators.average = None
        self.indicators.weight = 0.1
        self.indicators.ceil = 1.0
        self.indicators.face_cascade = CascadeClassifier(data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.indicators.iris_cascade = CascadeClassifier(data.haarcascades + 'haarcascade_eye.xml')
        self.indicators.body_cascade = CascadeClassifier(data.haarcascades + 'haarcascade_upperbody.xml')
        # Collectors
        self.image_collector = ImageCollector(self.address)
        self.frame_collector = FrameCollector(self.address)
        self.image_collector.start()
        self.frame_collector.start()

    # 0 : Add frame to stream
    #   i : If movement_detected
    #       i : If face_detected
    #           i : Add Frame to ImageCollector
    #   ii : Push to Stack
    # 1 : Output Feedback to Frame
    # 2 : Export Stack to Video
    #   i : Check timing parameters are triggered
    #   ii : Pop frames from stack
    #   iii : Construct video from frames
    #   iv : Upload video to S3 bucket
    # - : Export Frame Collectors Images (concurrently managed)
    #   i : Flush Frame Collector
    #   ii : Retrieve Images
    #   iii : Upload images to S3 bucket
    #   iv : Make call to API Gateway to trigger DetectIntruder lambda function on given images
    async def put(self, frame):
        now = time_now()
        self.triggers.is_movement = False
        self.triggers.is_person = False

        self.current_frame = resize(frame, (self.width, self.height))

        # Detect Movement in Current Frame
        if self.detect_movement():
            self.triggers.is_movement = True
            self.triggers.movement_timer = now + 1500
        # Check if there was any Recent Movement
        if now <= self.triggers.movement_timer:
            # Detect Face in Current Frame
            if self.detect_person():
                self.triggers.is_person = True
                await self.feedback_person()
                self.frame_collector.collect(frame, Tag.ALERT)
                self.image_collector.collect(frame)
            elif self.detect_movement:
                self.frame_collector.collect(frame, Tag.ACTIVITY)
            await self.feedback_movement()
        else:
            self.frame_collector.collect(frame, Tag.PERIODIC)

        # Within Clip Record Timeframe
        if self.config.start_time < now:
            self.stack.append(self.current_frame)
            # Past Clip Record Timeframe
            if self.config.stop_time < now:
                self.config.start_time = self.config.stop_time + self.config.gap_length
                self.config.stop_time = self.config.start_time + self.config.clip_length

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
        difference = cvtColor(absdiff(
            self.current_frame,
            convertScaleAbs(self.indicators.average)
        ), COLOR_BGR2GRAY)
        thresh = erode(
            dilate(
                threshold(difference, 70, 255, THRESH_BINARY)[1],
                None,
                iterations=2
            ), None, iterations=1
        )
        self.feedback.contours = grab_contours(
            findContours(
                thresh,
                RETR_EXTERNAL,
                CHAIN_APPROX_SIMPLE
            )
        )
        current_surface_area = 0.0
        for contour in self.feedback.contours:
            current_surface_area += contourArea(contour)

        if current_surface_area > self.indicators.ceil:
            self.indicators.ceil *= 1.05
            return True
        self.indicators.ceil *= 0.95
        return False

    # Detects Persons Face in Frame
    #   Returns True if Face Present
    #   Fills Feedback Buffer for Faces
    def detect_person(self):
        grey = cvtColor(self.current_frame, COLOR_BGR2GRAY)

        self.feedback.faces = self.indicators.face_cascade.detectMultiScale(
            grey,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(int(self.width * 0.05), int(self.height * 0.05))  # square must be 10% of screens size
        )

        for (x, y, w, h) in self.feedback.faces:
            self.feedback.irides = self.indicators.iris_cascade.detectMultiScale(
                grey[y:y+h, x:x+w],
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(int(self.width * 0.01), int(self.height * 0.01))
            )

        if len(self.feedback.faces) < 1 or len(self.feedback.irides) < 2:
            return False
            # self.feedback.faces = []
            # self.feedback.irides = []
            # self.feedback.bodies = self.indicators.body_cascade.detectMultiScale(
            #     grey,
            #     scaleFactor=1.05,
            #     minNeighbors=8,
            #     minSize=(int(self.width * 0.1), int(self.height * 0.1))  # square must be 10% of screens size
            # )
            # return len(self.feedback.bodies) > 0
        return True

    # Draws Movement Feedback to Frame
    async def feedback_movement(self):
        drawContours(self.current_frame, self.feedback.contours, -1, (0, 255, 0), 1)

    # Draws Persons Face Feedback to Frame
    async def feedback_person(self):
        if len(self.feedback.faces) > 0:
            for (x, y, w, h) in self.feedback.faces:
                rectangle(self.current_frame, (x, y), (x+w, y+h), (255, 0, 0), 1)
                for (ex, ey, ew, eh) in self.feedback.irides:
                    if ey + (eh / 2) < y + (h / 2):
                        rectangle(self.current_frame[y:y+h, x:x+w], (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)
        # elif len(self.feedback.bodies) > 0:
        #     for (x, y, w, h) in self.feedback.bodies:
        #         rectangle(self.current_frame, (x, y), (x+w, y+h), (255, 0, 0), 1)

    def size(self, width, height):
        (self.width, self.height) = (int(width), int(height))
