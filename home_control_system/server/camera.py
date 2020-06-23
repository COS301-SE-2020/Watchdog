import cv2
import threading
from .stream.stream import Stream
from .stream.frame import time_now

PROTOCOLS = ['', 'rstp', 'http', 'https']


# Camera connector
class Camera(threading.Thread):
    def __init__(self, address, port, path, location):
        threading.Thread.__init__(self)
        # Stream Management Object
        self.stream = Stream(self)
        # Camera Physical Location
        self.location = location
        # Camera IP Address
        self.address = address
        # Camera Address Port
        self.port = port
        # Camera Address Path (if necessary)
        self.path = path
        # Camera Connection Protocol
        self.protocol = ''
        # Live Boolean Spin Variable
        self.live = False
        # Camera Stream Connection
        self.connection = None
        # Camera Current Frame
        self.current_frame = None
        # Is IP Camera Connected
        self.is_connected = False
        # Is Movement Detected in Current Frame
        self.is_movement = False
        # Is Person Detected in Current Frame
        self.is_person = False

    # Start thread
    def run(self):
        print("Starting Camera Client [" + self.get_url() + "] Location:" + self.location)
        self.connect(self.protocol)
        self.live = True
        while(self.live):
            self.update()
        self.disconnect()
        print("Camera Client Stopped [" + self.get_url() + "] Location:" + self.location)

    # Stop thread
    def stop(self):
        self.live = False

    # Connect to IP Camera
    def connect(self, protocol=''):
        # new protocol used
        if self.protocol != protocol:
            self.is_connected = False
            self.protocol = protocol
        # check not already connected
        if not self.is_connected:
            self.connection = cv2.VideoCapture(self.get_url(True))
            self.connection.set(cv2.CAP_PROP_FPS, 30)
            if self.connection.isOpened():
                print("Connected to IP Camera [" + self.get_url() + "]")
                self.is_connected = True
            else:
                print("Failed to connect to IP Camera [" + self.get_url() + "]")
                self.is_connected = False
                # after a few tries, change protocol before retrying
        return self.is_connected

    # Disconnect from IP Camera
    def disconnect(self):
        # check connected
        if self.is_connected:
            self.connection.release()
            self.is_connected = False
        return not self.is_connected

    def check_connection(self):
        if (not self.is_connected) | (not self.connection.isOpened()):
            self.is_connected = False
        return self.is_connected

    # Update Camera Connection
    def update(self, frame_analysis=True):
        if(not self.is_connected):
            self.connect(self.protocol)

        fps = 20
        limit = 1000 / (fps)  # milliseconds
        begin = time_now()

        (grabbed, frame) = self.connection.read()
        if grabbed:
            # Adds Frame to Stream
            self.current_frame = frame
            self.stream.__in__(self.current_frame)
        else:
            self.check_connection()

        now = time_now()
        if now < begin + limit:
            # Outputs Feedback to Frame
            self.stream.__out__(self.current_frame)

    # Return Camera URL
    def get_url(self, print_protocol=False):
        url = self.address
        if self.port != '':
            url += ":" + self.port
        if self.path != '':
            url += "/" + self.path
        if print_protocol:
            if self.protocol != '':
                url = self.protocol + '://' + url
        return url

    # Set View Frame
    def set_frame(self, height, width):
        self.stream.size(width, height)
