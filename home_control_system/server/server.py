import threading
from .camera import Camera
from .stream.stream import collector


class Server(threading.Thread):
    def __init__(self, address, location='Home'):
        threading.Thread.__init__(self)
        self.live = False
        self.address = address
        self.location = location
        self.cameras = {}

    # adds a ip camera client to an allocated port on the server
    def add_camera(self, address, port='', path='', location='Room', protocol=''):
        if not self.check_address(address):
            print("Adding camera " + str(address) + " - " + location)
            client = Camera(protocol, address, port, path, location)
            if client.is_connected:
                self.cameras[address] = client
            return client  # successfully added client
        return self.cameras[address]

    def check_address(self, address):
        # quick check
        if f"{self.address}" in self.cameras:
            return True
        # double check
        for camera_address, camera_client in self.cameras.items():
            if camera_client.address == address:
                return True
        return False

    # starts the server
    def run(self):
        if self.cameras.__len__() == 0:
            print("Error: There are currently no ip cameras detected.")
        # Start Streams
        for address, client in self.cameras.items():
            client.start()

    # stops the server
    def stops(self):
        for address, client in self.cameras.items():
            client.stop()
        collector.live = False

    def client_stats(self, address):
        stats = {}
        stats['is_connected'] = self.cameras[address].is_connected
        stats['is_movement'] = self.cameras[address].is_movement
        stats['is_person'] = self.cameras[address].is_person
        stats['is_frames'] = self.cameras[address].current_frame is not None
        return stats

    def __str__(self):
        server = 'Home Control Panel Server' + '\n'
        server += '\t' + 'Located @ [label:' + self.location + ']' + '\n'
        server += '\t' + 'Serving @ [url:' + self.address + ']' + '\n'
        server += '\t' + 'Hosting [' + str(len(self.cameras)) + ' IP Camera(s)]' + '\n'
        for address, client in self.cameras.items():
            server += '\t\t' + str(client) + '\n'
        return server
