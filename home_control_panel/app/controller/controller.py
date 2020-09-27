import os
import time
import json
import random
import threading
from hashlib import sha256
from .camera import Camera
from .location import Location
from ...service import services
from ...service import connection

conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']


# Camera Controller Class
#   Manages all camera and location objects
#   Host stream server connection
#   Manages Main Connection and Camera Connections
class CameraController(threading.Thread):
    def __init__(self, app=None):
        threading.Thread.__init__(self)
        # Reference to UI Application
        self.app = app
        # live indicator
        self.live = False
        # Mapping of camera address to camera objects
        self.cameras = {}
        # Mapping of location names to location objects
        self.locations = {}

    # Starts the controller
    def run(self):
        if self.cameras.__len__() == 0:
            print("There are currently no ip cameras detected...")
        self.live = True
        # Start Loaded Cameras
        for address, client in self.cameras.items():
            client.start()
        # Start Client Controllers Stream Connection Management
        while(self.live):
            for address, client in self.cameras.items():
                if not client.check_connection():
                    self.app.repair_camera(client.location, client.id, client.name, client.address, client.port, client.path, client.protocol)
                    # TODO: Check if Repaired in real time and update DB
            if self.connect():
                time.sleep()

    # Stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()

    # Connect to Livestream Server
    def connect(self):
        if self.client is None:
            self.client = connection.Producer(services.User.get_instance().user_id, services.User.get_instance().hcp_id, self)
        if not self.client.connected:
            exp_wait = 1
            while not self.client.connect():
                time.sleep(exp_wait ^ exp_wait)
                exp_wait += 1
                if exp_wait > 6:
                    return False
        self.client.authorize()
        return True

    # Starts the given cameras livestreams, stops all the others
    def start_streams(self, camera_list):
        if self.connect():
            for address, camera in self.cameras.items():
                if camera.id in camera_list:
                    camera.start_stream(self.client)
                else:
                    camera.stop_stream()
        else:
            self.stop_streams()

    # Stops all camera streams
    def stop_streams(self):
        for address, camera in self.cameras.items():
            camera.stop_stream()

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
                            camera['name'],
                            camera['address'],
                            camera['port'],
                            camera['path'],
                            camera['protocol']
                        )
                        if loaded_camera is None:
                            # Camera Failed to Connect, Delete from DB and Ask User to Fix Details
                            services.remove_camera(location, camera_id)
                            self.app.repair_camera(location, camera_id, camera['name'], camera['address'], camera['port'], camera['path'], camera['protocol'])
                            services.upload_camera(camera_id, {
                                "location": location,
                                "name": camera['name'],
                                "address": camera['address'],
                                "port": camera['port'],
                                "path": camera['path'],
                                "protocol": camera['protocol']
                            })
            return True
        return False

    # Returns the list of cameras for a given location
    def get_cameras(self, location):
        cameras = []
        for address, camera in self.locations[location].cameras.items():
            cameras.append(camera)
        return cameras

    # Returns the list of locations
    def get_locations(self):
        locations = []
        for location, location_object in self.locations.items():
            locations.append(location)
        return locations

    def get_camera_ids(self):
        # Build List of Camera ID's
        camera_ids = []
        for address, camera in self.cameras.items():
            camera_ids.append(camera.id)
        return camera_ids

    # Loads in an Existing location
    def load_location(self, label):
        if label not in self.locations:
            self.locations[label] = Location(label, self)
            self.app.add_location(label)

    # Loads in an Existing Camera
    def load_camera(self, location, camera_id, name, address, port, path, protocol):
        if location in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location)
            if client.is_connected:
                print("Loading camera " + str(client))
                self.cameras[address] = client
                self.locations[location].add_camera(client)
                self.app.add_camera(location, camera_id, name, address, port, path, protocol)
                self.app.attach_stream(camera_id, self.cameras[address].stream)
                return client  # successfully added client
        return None

    # Adds a new Location
    def add_location(self, label):
        if label not in self.locations:
            self.locations[label] = Location(label, self)
            self.app.add_location(label)
            # TODO: Added a service function for adding a location without cameras

    # Adds a new Camera and Inserts it into database
    def add_camera(self, location, name, address, port, path, protocol):
        camera_id = 'c' + str(sha256((str(random.getrandbits(128))).encode('ascii')).hexdigest())
        if location in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location)
            if client.is_connected:
                print("Adding camera " + str(client))

                response = services.upload_camera(client.id, client.get_metadata())
                if response is not None and response.status_code != 200:
                    print('Warning: Camera not uploaded!')

                self.cameras[address] = client
                self.cameras[address].start()

                self.locations[location].add_camera(self.cameras[address])
                self.client.authorize()
                self.app.add_camera(location, camera_id, name, address, port, path, protocol)
                return self.cameras[address]  # successfully added client
            else:
                print('Warning: Could not connect to camera', '[', camera_id, name, ']')
        return None

    # Returns stats for a given camera address
    def client_stats(self, address):
        stats = {}
        stats['is_frames'] = self.cameras[address].stream.current_frame is not None
        stats['is_movement'] = self.cameras[address].stream.triggers.is_movement
        stats['is_person'] = self.cameras[address].stream.triggers.is_person
        stats['is_connected'] = self.cameras[address].is_connected
        return stats

    def __str__(self):
        controller = 'Home Control Panel' + '\n'
        controller += '\t' + 'Site @ [label:' + site_label + ']' + '\n'
        controller += '\t' + 'Hosting [' + str(len(self.cameras)) + ' IP Camera(s)]' + '\n'
        for address, client in self.cameras.items():
            controller += '\t\t' + str(client) + '\n'
        return controller
