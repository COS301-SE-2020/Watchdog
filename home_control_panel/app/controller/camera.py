import os
import json
import cv2
import threading
from .stream.stream import Stream
from ...service import connection
from ...service import services

conf = json.loads(os.environ['config'])
PROTOCOLS = ['', 'rstp', 'http', 'https']
FPS = conf['video']['frames_per_second']
(RES_X, RES_Y) = (conf['video']['resolution']['width'], conf['video']['resolution']['height'])


# Camera connector
class Camera(threading.Thread):
    def __init__(self, id, protocol='', name='', address='', port='', path='', location=''):
        threading.Thread.__init__(self)
        # Given camera id
        self.id = id
        # Camera Name
        self.name = name
        # Camera Address Port
        self.port = port
        # Camera Address Path
        self.path = path
        # Camera IP Address
        self.address = address
        # Camera Connection Protocol
        self.protocol = protocol
        # Camera Physical Location
        self.location = location
        # Live Boolean Spin Variable
        self.live = False
        # Connection
        self.connection = None
        # Connection for Outgoing broadcast
        self.stream_connection = None
        # Is IP Camera Connected
        self.is_connected = False
        # Stream Management Object
        self.stream = Stream(self.id, self.address, (RES_X, RES_Y))
        # Connect to Camera
        self.connect()

    # Start thread
    def run(self):
        print("Starting Camera Client " + str(self))
        # Set to Live
        self.live = True
        # Update stream while live
        while(self.live):
            self.update()

    # Stop thread
    def stop(self):
        self.live = False
        self.disconnect()

    # Activates Livestream for Stream Object by providing a connection
    def start_stream(self):
        self.stream_connection = connection.RTCConnectionHandler(
            self.id,
            services.User.get_instance().user_id,
            self.get_url(True)
        )
        return self.stream_connection

    # Deactivates Livestream for Stream Object by removing connection
    def stop_stream(self):
        self.stream_connection = None

    def check_stream(self):
        if self.stream_connection is not None and self.stream_connection.is_connected:
            return True
        return False

    # Connect to IP Camera
    def connect(self):
        # check not already connected
        if self.connection is None or not self.connection.isOpened():
            # Camera Stream Connection
            self.connection = cv2.VideoCapture(self.get_url(True))
            self.connection.set(cv2.CAP_PROP_FPS, FPS)
            self.connection.set(cv2.CAP_PROP_FRAME_WIDTH, RES_X)
            self.connection.set(cv2.CAP_PROP_FRAME_HEIGHT, RES_Y)
            if self.connection.isOpened():
                print("Connected to IP Camera [" + str(self.get_url()) + "]")
                self.is_connected = True
            else:
                print("Failed to connect to IP Camera [" + str(self.get_url()) + "]")
                self.is_connected = False
                # after a few tries, change protocol before retrying
        return self.is_connected

    # Disconnect from IP Camera
    def disconnect(self):
        # check connected
        if self.is_connected:
            self.connection.release()
            self.is_connected = False
            self.connection = None
        return not self.is_connected

    # Update Camera Connection with new Frame and put in the stream
    def update(self):
        if not self.is_connected or self.connection is None:
            self.connect()
            return
        (grabbed, frame) = self.connection.read()
        if grabbed:
            self.stream.put(frame)
        else:
            self.disconnect()
            self.connect()

    def check_connection(self):
        if not self.is_connected or self.connection is None or not self.connection.isOpened():
            self.connect()
        return self.is_connected

    # Return Camera URL
    def get_url(self, print_protocol=False):
        if(self.address.isnumeric()):
            return int(self.address)
        url = self.address
        if self.port != '':
            url += ":" + self.port
        if self.path != '':
            url += "/" + self.path
        if print_protocol:
            if self.protocol != '':
                url = self.protocol + '://' + url
        return url

    def get_metadata(self):
        return {
            "location": self.location,
            "name": self.name,
            "address": self.address,
            "port": self.port,
            "path": self.path,
            "protocol": self.protocol
        }

    def __str__(self):
        camera = '[address:' + str(self.get_url()) + ']'
        if self.protocol != '':
            camera = '[protocol:' + self.protocol + ']' + camera
        if self.location != '':
            camera = '[location:' + self.location + ']' + camera
        return camera
