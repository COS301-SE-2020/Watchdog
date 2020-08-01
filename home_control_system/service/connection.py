import cv2
import base64
import random
import socketio

CLIENT_KEY = 'supersecure'


# Front-End Client Asbtract Class
class Connection:
    def __init__(self, user_id):
        self.id = self.generate_id(self)
        self.user_id = user_id
        self.socket = socketio.Client()
        self.socket.connect('http://127.0.0.1:8008')

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
    def __init__(self, user_id, controller):
        super(Producer, self).__init__(user_id)
        self.active = False
        self.camera_list = []
        self.controller = controller
        self.socket.emit('authorize', {'user_id': self.user_id, 'client_type': 'producer', 'client_key': CLIENT_KEY})

    # Start HCP Client Producer
    def activate(self, camera_list):
        self.active = True
        self.camera_list = camera_list
        self.controller.start_streams(self.camera_list)

    # Stop HCP Client Producer
    def deactivate(self):
        self.active = False
        self.camera_list = None
        self.controller.stop_streams()

    # Send frame through to Server
    def produce(self, camera_id, frame_px):
        if self.active and camera_id in self.camera_list:
            retval, buffer = cv2.imencode('.jpg', frame_px)
            frame = str(base64.b64encode(buffer))
            self.socket.emit('produce-frame', {'camera_id': camera_id, 'frame': frame})
