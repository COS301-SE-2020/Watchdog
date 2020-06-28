import cv2
import threading
from .stream.stream import Stream

PROTOCOLS = ['', 'rstp', 'http', 'https']
FPS = 20
(RES_X, RES_Y) = (900, 500)

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
        # Stream Management Object
        self.stream = Stream(self.address, (RES_X, RES_Y))
        # Stream View GUI Object
        self.stream_view = None
        # Connect to Camera
        self.connect()

    # Start thread
    def run(self):
        print("Starting Camera Client " + str(self))
        # Spin until stream has been defined
        while self.stream is None:
            self.live = False
        # Update stream while live
        self.live = True
        while(self.live):
            self.update()
        # Disconnect after the stream has been stopped
        self.disconnect()
        print("Camera Client Stopped " + str(self))

    # Update Camera Connection
    def update(self):
        if(not self.is_connected):
            self.connect()
        (grabbed, frame) = self.connection.read()
        if grabbed:
            self.stream.put(frame)
        else:
            self.check_connection()

    # Stop thread
    def stop(self):
        self.live = False
        self.disconnect()

    # Connect to IP Camera
    def connect(self):
        # check not already connected
        if not self.is_connected:
            # Camera Stream Connection
            self.connection = cv2.VideoCapture(self.get_url(True))
            self.connection.set(cv2.CAP_PROP_FPS, FPS)
            self.connection.set(cv2.CAP_PROP_FRAME_WIDTH, RES_X)
            self.connection.set(cv2.CAP_PROP_FRAME_HEIGHT, RES_Y)
            if self.connection.isOpened():
                print("Connected to IP Camera [" + self.get_url() + "]")
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

    def __str__(self):
        camera = '[address:' + self.get_url() + ']'
        if self.protocol != '':
            camera = '[protocol:' + self.protocol + ']' + camera
        if self.location != '':
            camera = '[location:' + self.location + ']' + camera
        return camera
