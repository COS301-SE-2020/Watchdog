import copy
import asyncio
import cv2 as cv
from numpy import array
from imutils import grab_contours
from cv2 import (
    CascadeClassifier,
    VideoWriter,
    VideoWriter_fourcc,
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
    absdiff
)
# from service.upload import upload_api
from .frame_collector import FrameCollector
from .frame import (
    time_now,
    hash_id
)

# Stream
#   In-Out Frame Processing Pipe
#      Does Movement Detection & Face Detection
#      Periodically Stacks frames then Exports Result Video
#      Handles Intruder Alert Frames then Adds to FrameCollector which Exports the Result Image
#   Upload the Result Videos and Images to S3 Bucket
class Stream:
    def __init__(self, camera):
        self.camera = camera
        self.collector = FrameCollector()
        self.stack = []
        (self.height, self.width) = (480, 360)
        # Indicators for Analysis
        self.indicators = {}
        self.indicators['average'] = None
        self.indicators['weight'] = 0.05
        self.indicators['ceil'] = 1.5
        self.indicators['cascade'] = CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Feedback to be Outputted to Frame
        self.feedback = {}
        self.feedback['contours'] = None
        self.feedback['rectangles'] = None
        # Checks
        self.triggers = {}
        self.triggers['is_movement'] = False
        self.triggers['is_person'] = False
        self.triggers['was_movement'] = False
        self.triggers['was_person'] = False
        # Config for Periodic Video
        self.config = {}
        self.config['frames_per_second'] = 30.0  # seconds
        self.config['clip_length'] = 10000  # milliseconds
        self.config['gap_length'] = 20000  # milliseconds
        self.config['start_time'] = time_now()
        self.config['stop_time'] = time_now() + self.config['clip_length']

    # Add frame to stream
    #   Push to Stack
    #   If movement_detected
    #       If face_detected
    #           Add Frame to FrameCollector
    def __in__(self, frame):
        self.triggers['was_movement'] = self.triggers['is_movement']
        self.triggers['was_person'] = self.triggers['is_person']
        if self.detect_movement(frame):
            self.camera.is_movement = self.triggers['is_movement'] = True
        else:
            self.camera.is_movement = self.triggers['is_movement'] = False
        if self.triggers['is_movement'] | self.triggers['was_movement']:
            if self.detect_person(frame):
                self.camera.is_person = self.triggers['is_person'] = True
                self.collector.collect(frame, self.camera.address)
            else:
                self.camera.is_person = self.triggers['is_person'] = False
        return frame

    # 0 : Output Feedback to Frame
    # 1 : Export Stack to Video
    #   i : Check timing parameters are triggered
    #   ii : Pop frames from stack
    #   iii : Construct video from frames
    #   iv : Upload video to S3 bucket
    # 2 : Export Frame Collectors Images
    #   i : Flush Frame Collector
    #   ii : Retrieve Images
    #   iii : Upload images to S3 bucket
    #   iv : Make call to API Gateway to trigger DetectIntruder lambda function on given images
    def __out__(self, frame):
        if self.triggers['is_person']:
            frame = self.feedback_person(frame)
            self.collector.flush()
        elif self.triggers['is_movement']:
            frame = self.feedback_movement(frame)
        # check time
        now = time_now()
        # Within Clip Record Timeframe
        if self.config['start_time'] < now:
            self.stack.append(frame)
            # Past Clip Record Timeframe
            if self.config['stop_time'] < now:
                self.config['start_time'] = self.config['stop_time'] + self.config['gap_length']
                self.config['stop_time'] = self.config['start_time'] + self.config['clip_length']
                asyncio.run(self.export_video())

        return frame

    def size(self, width, height):
        (self.height, self.width) = (width, height)

    # Detects Movement in Frame
    #   Returns True if Movement
    #   Fills Feedback Buffer for Movement
    def detect_movement(self, frame):
        if self.indicators['average'] is None:
            self.indicators['average'] = array(frame, float)
        accumulateWeighted(
            frame,
            self.indicators['average'],
            self.indicators['weight']
        )
        difference = cvtColor(absdiff(
            frame,
            convertScaleAbs(self.indicators['average'])
        ), cv.COLOR_BGR2GRAY)
        thresh = erode(
            dilate(
                threshold(difference, 70, 255, cv.THRESH_BINARY)[1],
                None,
                iterations=2
            ), None, iterations=1
        )
        self.feedback['contours'] = grab_contours(
            findContours(
                thresh,
                cv.RETR_EXTERNAL,
                cv.CHAIN_APPROX_SIMPLE
            )
        )
        current_surface_area = 0.0
        for contour in self.feedback['contours']:
            current_surface_area += contourArea(contour)
        
        if current_surface_area > self.indicators['ceil']:
            self.indicators['ceil'] *= 1.1
            self.indicators['weight'] *= 0.9
            return True
        self.indicators['ceil'] *= 0.9
        self.indicators['weight'] *= 1.1
        return False

    # Detects Persons Face in Frame
    #   Returns True if Face Present
    #   Fills Feedback Buffer for Faces
    def detect_person(self, frame):
        self.feedback['rectangles'] = self.indicators['cascade'].detectMultiScale(
            cvtColor(frame, cv.COLOR_BGR2GRAY),
            scaleFactor=1.5,
            minNeighbors=5
        )
        return len(self.feedback['rectangles']) > 0  # Return True if List Not Empty

    # Draws Movement Feedback to Frame
    def feedback_movement(self, frame):
        if self.feedback['contours'] is not None:
            drawContours(frame, self.feedback['contours'], -1, (0, 255, 0), 1)
        return frame

    # Draws Persons Face Feedback to Frame
    def feedback_person(self, frame):
        if self.feedback['rectangles'] is not None:
            for (x, y, w, h) in self.feedback['rectangles']:
                rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 15)
        return frame

    async def export_video(self):
        name = 'data/temp/video/' + hash_id(time_now(), self.camera.address) + '.avi'
        print("Exporting Video [" + name + "]")

        (h, w) = self.camera.current_frame.shape[:2]
        stack = copy.deepcopy(self.stack)
        self.stack.clear()

        file = VideoWriter(name, VideoWriter_fourcc(*"MJPG"), self.config['frames_per_second'], (w, h), True)
        for index in range(len(stack)):
            file.write(stack[index])
        file.release()

        # send to s3

    async def export_image(self, image):
        name = 'data/temp/image/' + hash_id(time_now(), self.camera.address) + '.jpg'
        print("Exporting Video [" + name + "]")

        # send to s3
