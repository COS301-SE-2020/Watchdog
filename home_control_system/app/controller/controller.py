import os
import json
import threading
from .camera import Camera


conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']


class CameraController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.live = False
        self.cameras = {}

    # adds a ip camera client to an allocated port on the controller
    def add_camera(self, camera_id, address, port='', path='', location='Room', protocol=''):
        if not self.check_address(address):
            print("Adding camera " + str(address) + " - " + location)
            client = Camera(camera_id, protocol, address, port, path, location)
            if client.is_connected:
                self.cameras[address] = client
            if self.live:
                client.start()
            return client  # successfully added client
        return None

    def check_address(self, address):
        # quick check
        if f"{address}" in self.cameras:
            return True
        # double check
        for camera_address, camera_client in self.cameras.items():
            if camera_client.address == address:
                return True
        return False

    # starts the controller
    def run(self):
        self.live = True
        if self.cameras.__len__() == 0:
            print("There are currently no ip cameras detected...")
        # Start Streams
        for address, client in self.cameras.items():
            client.start()

    # stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()

    def client_stats(self, address):
        stats = {}
        stats['is_connected'] = self.cameras[address].is_connected
        stats['is_movement'] = self.cameras[address].stream.triggers.is_movement
        stats['is_person'] = self.cameras[address].stream.triggers.is_person
        stats['is_frames'] = self.cameras[address].stream.current_frame is not None
        return stats

    def __str__(self):
        controller = 'Home Control Panel' + '\n'
        controller += '\t' + 'Site @ [label:' + site_label + ']' + '\n'
        controller += '\t' + 'Hosting [' + str(len(self.cameras)) + ' IP Camera(s)]' + '\n'
        for address, client in self.cameras.items():
            controller += '\t\t' + str(client) + '\n'
        return controller
