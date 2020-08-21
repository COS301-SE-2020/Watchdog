import os
import time
import json
import random
import threading
from hashlib import sha256
from service import services
from service import connection
from .camera import Camera
from .location import Location

conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']


class CameraController(threading.Thread):
    def __init__(self, app=None):
        threading.Thread.__init__(self)
        self.client = None
        self.live = False
        self.locations = {}
        self.cameras = {}
        self.app = app

    # Called at Start, Pass in UI Window for UI Setup
    def setup_environment(self):
        print('Loading Environment...')
        locations = services.get_camera_setup()
        if locations is not None:
            for location, cameras in locations.items():
                self.load_location(location)
                if cameras is not None:
                    for camera_id, camera in cameras.items():
                        loaded_camera = self.load_camera(
                            location,
                            camera_id,
                            camera['address'],
                            camera['port'],
                            camera['path'],
                            camera['protocol']
                        )
                        if loaded_camera is None:
                            if self.app is not None:
                                self.app.window.fix_camera('', camera['address'], camera['port'], camera['protocol'], camera['path'])
                            services.remove_camera(location, camera_id)
            self.update_widgets()
            return True
        return False

    def update_widgets(self):
        if self.app is not None:
            self.app.window.set_locations(self.get_locations())
            self.app.window.set_cameras(self.get_cameras(location=self.app.current_location))

    def get_cameras(self, location):
        cameras = []
        for address, camera in self.locations[location].cameras.items():
            cameras.append(camera)
        return cameras

    def get_locations(self):
        locations = []
        for location, location_object in self.locations.items():
            locations.append(location)
        return locations

    def load_location(self, label):
        if label not in self.locations:
            self.locations[label] = Location(label, self)
            self.app.change_location(label)

    def add_location(self, label):
        if label not in self.locations:
            self.locations[label] = Location(label, self)
            if self.app is not None:
                self.app.change_location(label)
            self.update_widgets()

    def load_camera(self, location, camera_id, address, port, path, protocol):
        if location in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, address, port, path, location)
            if client.is_connected:
                print("Loading camera " + str(client))
                self.cameras[address] = client
                self.locations[location].add_camera(client)
                return client  # successfully added client
        return None

    def add_camera(self, location, address, port, path, protocol):
        camera_id = 'c' + str(sha256((str(random.getrandbits(128))).encode('ascii')).hexdigest())

        if location in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, address, port, path, location)

            if client.is_connected:
                print("Adding camera " + str(client))

                response = services.upload_camera(client.id, client.get_metadata())
                if response is not None and response.status_code != 200:
                    return None

                self.cameras[address] = client
                self.locations[location].add_camera(client)

                if self.live:
                    client.start()

                self.update_widgets()
                return client  # successfully added client
        return None

    # starts the controller
    def run(self):
        self.live = True
        if self.cameras.__len__() == 0:
            print("There are currently no ip cameras detected...")
        # Start Streams
        for address, client in self.cameras.items():
            client.start()

        camera_ids = []

        for address, camera in self.cameras.items():
            camera_ids.append(camera.id)

        # print('sending... ', camera_ids)
        # self.client = connection.Producer(user_id, producer_id, camera_ids, self)

        if self.app is not None:
            user_id = services.User.get_instance().user_id
            producer_id = services.User.get_instance().hcp_id
            print('sending... ', camera_ids)
            self.client = connection.Producer(user_id, producer_id, camera_ids, self)
            while(True):
                self.app.window.home.view.grid.viewer.refresh()
                time.sleep(1 / 30)

    # stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()

    def start_streams(self, camera_list):
        if self.client is not None:
            for address, camera in self.cameras.items():
                if camera.id in camera_list:
                    camera.start_stream(self.client)
                else:
                    camera.stop_stream()

    def stop_streams(self):
        for address, camera in self.cameras.items():
            camera.stop_stream()

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
