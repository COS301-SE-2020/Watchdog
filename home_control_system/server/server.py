import threading
from cv2 import waitKey
from .camera import Camera
from .stream.frame import time_now

class Server(threading.Thread):
    def __init__(self, address, location='Home'):
        threading.Thread.__init__(self)
        self.live = False
        self.address = address
        self.location = location
        self.cameras = {}
        (self.height, self.width) = (360, 480)  # To be moved

    # adds a ip camera client to an allocated port on the server
    def add_camera(self, address, port='', path='', location='Room', protocol=''):
        if not self.check_address(address):
            print("Adding camera " + address + " - " + location)
            client = Camera(address, port, path, location)
            # Set Stream Resolution
            # client.set_stream_dimensions(self.height / len(self.cameras), self.width / len(self.cameras))
            client.connect(protocol)
            if client.is_connected:
                self.cameras[address] = client
            return client  # successfully added client
        return None

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

        self.live = True
        while self.live:
            start = time_now()
            # end = start + 16.67
            try:
                for address, client in self.cameras.items():
                    client.update_stream_view()
                waitKey(1)
                now = time_now()
                # wait = 16.67 - (now - start)
                while 16.67 > (now - start):
                    now = time_now()
            except KeyboardInterrupt:
                print("Server Stopped")
                break

        for address, client in self.cameras.items():
            client.stop()

    def client_stats(self, address):
        stats = {}
        stats['is_connected'] = self.cameras[address].is_connected
        stats['is_movement'] = self.cameras[address].is_movement
        stats['is_person'] = self.cameras[address].is_person
        stats['is_frames'] = self.cameras[address].current_frame is not None
        return stats
