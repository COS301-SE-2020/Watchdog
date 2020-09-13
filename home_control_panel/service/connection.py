import cv2
import base64
import random
import socketio
from . import config
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

conf = config.configure()
CLIENT_KEY = conf['services']['client']['key']
SERVER_URL = conf['services']['stream_url']


# Front-End Client Asbtract Class
class Connection:
    def __init__(self, user_id):
        self.id = self.generate_id(self)
        self.user_id = user_id
        self.socket = socketio.Client(ssl_verify=False)

        try:
            self.socket.connect(SERVER_URL)
            self.connect = True
        except socketio.exceptions.ConnectionError:
            print("Failed to connect to stream server")
            self.connect = False

        # Data : { user_id : string, camera_list : string }
        @self.socket.on('activate-broadcast')
        def activate_broadcast(data):
            print('activating broadcast ... ' + str(data))
            self.activate(data['camera_list'])

        # Data : { user_id : string, camera_list : string }
        @self.socket.on('deactivate-broadcast')
        def deactivate_broadcast(data):
            print('deactivating broadcast ... ' + str(data))
            self.deactivate()

        # Data : { user_id : string, frame : string }
        @self.socket.on('consume-frame')
        def consume_frame(data):
            print('consuming frame ... ' + str(data))
            image = data['frame']
            self.consume(image)

    @staticmethod
    def generate_id(user):
        id = 'u' + str(random.getrandbits(128))
        return id


# Front-End Producer Client
class Producer(Connection):
    def __init__(self, user_id, producer_id, camera_ids, controller):
        super(Producer, self).__init__(user_id)
        self.active = False
        self.camera_list = camera_ids
        self.controller = controller
        self.producer_id = producer_id
        self.authorize()

    def add_camera(self, camera):
        if camera not in self.camera_list:
            self.camera_list.append(camera)
            self.authorize()

    def authorize(self):
        print('Cameras:', self.camera_list)
        if self.connect:
            self.socket.emit('authorize', {
                'user_id': self.user_id,
                'client_type': 'producer',
                'producer_id': self.producer_id,
                'available_cameras': self.camera_list,
                'client_key': CLIENT_KEY
            })

    # Start HCP Client Producer
    def activate(self, camera_list):
        self.active = True
        self.controller.start_streams(camera_list)

    # Stop HCP Client Producer
    def deactivate(self):
        self.active = False
        self.controller.stop_streams()

    # Send frame through to Server
    def produce(self, camera_id, frame_px):
        if self.connect:
            if self.active and camera_id in self.camera_list:
                retval, buffer = cv2.imencode('.jpg', frame_px)
                frame = str(base64.b64encode(buffer))
                self.socket.emit('produce-frame', {'camera_id': camera_id, 'frame': frame})
