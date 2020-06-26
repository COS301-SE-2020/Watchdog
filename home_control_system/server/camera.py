import cv2
import asyncio
import threading
from .stream.stream import Stream
# from .app.widgets import StreamView
from .stream.frame import time_now

PROTOCOLS = ['', 'rstp', 'http', 'https']


# Camera connector
class Camera(threading.Thread):
    def __init__(self, protocol, address, port, path, location):
        threading.Thread.__init__(self)
        # Camera Physical Location
        self.location = location
        # Camera IP Address
        self.address = address
        # Camera Address Port
        self.port = port
        # Camera Address Path (if necessary)
        self.path = path
        # Camera Connection Protocol
        self.protocol = protocol
        # Live Boolean Spin Variable
        self.live = False
        # Is IP Camera Connected
        self.is_connected = False
        # Is Movement Detected in Current Frame
        self.is_movement = False
        # Is Person Detected in Current Frame
        self.is_person = False
        # Stream View GUI Object
        self.stream_view = None
        # Stream Management Object
        self.stream = None
        # Camera Stream Connection
        self.connection = cv2.VideoCapture(self.get_url(True))
        # Connect to Camera
        self.connect()

    # Start thread
    def run(self):
        print("Starting Camera Client [" + self.get_url() + "] Location:" + self.location)
        self.connect(self.protocol)

        while self.stream is None:
            print('Waiting...')

        self.live = True
        while(self.live):
            self.update()

        self.disconnect()
        print("Camera Client Stopped [" + self.get_url() + "] Location:" + self.location)

    # Update Camera Connection
    def update(self):
        if(not self.is_connected):
            self.connect(self.protocol)
        (grabbed, frame) = self.connection.read()
        if grabbed:
            self.stream.__in__(frame)
        else:
            self.check_connection()

    # Stop thread
    def stop(self):
        self.live = False
        self.disconnect()

    # Connect to IP Camera
    def connect(self, protocol=''):
        # new protocol used
        if self.protocol != protocol:
            self.is_connected = False
            self.protocol = protocol
        # check not already connected
        if not self.is_connected:
            # self.connection = cv2.VideoCapture(self.get_url(True))
            self.connection.set(cv2.CAP_PROP_FPS, 1)
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

    # Return Camera URL
    def get_url(self, print_protocol=False):
        if(self.address is int):
            return self.address
        url = self.address
        if self.port != '':
            url += ":" + self.port
        if self.path != '':
            url += "/" + self.path
        if print_protocol:
            if self.protocol != '':
                url = self.protocol + '://' + url
        return url

    def visit_stream_view(self):
        if self.stream_view is not None:
            return self.stream_view.refresh()

    # Initialize the stream view
    def init_stream(self, stream_view, width, height):
        self.stream = Stream(stream_view, self.address, width, height)
        self.connection.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.connection.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
