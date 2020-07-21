# Front-End Client Asbtract Class
class Client:
    users = {}

    def __init__(self, user_id, socket):
        self.id = self.generate_id(self)
        self.user_id = user_id
        self.socket = socket
        self.socket.connect('http://127.0.0.1:8008')

    @staticmethod
    def generate_id(user):
        id = 'u' + str(len(Client.users))
        Client.users[id] = user
        return id


# Front-End Producer Client
class Producer(Client):
    producers = {}

    def __init__(self, user_id, socket):
        super(Producer, self).__init__(user_id, socket)
        self.active = False
        self.socket.emit('authorize', {'user_id': self.user_id, 'client_type': 'producer', 'client_key': 1})
        Producer.producers[self.id] = self

    # Start HCP Client Producer
    def activate(self):
        self.active = True

    # Stop HCP Client Producer
    def deactivate(self):
        self.active = False

    # Send frame through to Server
    def produce(self, frame):
        if self.active:
            self.socket.emit('broadcast', {'frame': frame})

def start_broadcast(user_id):
    for id, user in Producer.producers.items():
        if user.user_id == user_id:
            user.activate()

def stop_broadcast(user_id):
    for id, user in Producer.producers.items():
        if user.user_id == user_id:
            user.deactivate()

def display_stream(user_id, image):
    for id, user in Consumer.consumers.items():
        if user.user_id == user_id:
            user.consume(image)
