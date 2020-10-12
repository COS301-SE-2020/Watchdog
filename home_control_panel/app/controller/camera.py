import os
import json
import platform
import threading
from aiortc import MediaStreamTrack
from aiortc.contrib.media import MediaPlayer
from .stream.stream import Stream
from ...service import connection
from ...service import services
from .controller import EVENT_LOOP

conf = json.loads(os.environ['config'])
PROTOCOLS = ['', 'rstp', 'http', 'https']
FPS = conf['video']['frames_per_second']
(RES_X, RES_Y) = (conf['video']['resolution']['width'], conf['video']['resolution']['height'])


class VideoStream(MediaStreamTrack):
    kind = "video"

    def __init__(self, track):
        super(MediaStreamTrack).__init__()  # don't forget this!
        self.track = track
        self.frame = None

    async def recv(self):
        self.frame = await self.track.recv()


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
        # Connection for Outgoing broadcast
        self.stream_connection = None
        # Is IP Camera Connected
        self.is_connected = False
        # Stream Management Object
        self.stream = Stream(self.id, self.address, (RES_X, RES_Y))
        #
        self.track = None
        #
        self.player = None
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
            services.User.get_instance().user_id,
            self
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
        if self.player is None:
            try:
                # options = {"framerate": "30", "video_size": "640x480"}
                url = self.get_url(True)
                if url == 0:
                    print('Connecting to Webcam...')
                    if platform.system() == 'Darwin':
                        self.player = MediaPlayer('default:none', format="avfoundation", options={"framerate": "30"})
                    else:
                        self.player = MediaPlayer("/dev/video0", format="v4l2")
                else:
                    self.player = MediaPlayer(self.get_url(True))

                self.track = VideoStream(self.player.video)
                print("Connected to IP Camera [" + str(self.get_url()) + "]")
                self.is_connected = True
            except Exception as e:
                self.track = None
                print("Failed to connect to IP Camera [" + str(self.get_url()) + "]")
                print(e)
                self.is_connected = False
        return self.is_connected

    # Disconnect from IP Camera
    def disconnect(self):
        # check connected
        if self.is_connected:
            self.connection = None
            self.is_connected = False
        return not self.is_connected

    # Update Camera Connection with new Frame and put in the stream
    def update(self):
        if not self.is_connected or self.player is None:
            self.connect()

        if self.track is not None:
            EVENT_LOOP.run_until_complete(self.track.recv())
            if self.track.frame is not None:
                self.stream.put(self.track.frame.to_ndarray(format="bgr24"))
        else:
            self.disconnect()

    def check_connection(self):
        if not self.is_connected or self.player is None:
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
