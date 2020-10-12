import asyncio
import os
import json
import time
import random
import threading
from hashlib import sha256
import nest_asyncio

nest_asyncio.apply()
EVENT_LOOP = asyncio.get_event_loop()
asyncio.set_event_loop(EVENT_LOOP)

from .location import Location
from ...service import services
from .camera import Camera

conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']


# Camera Controller Class
#   Manages all camera and location objects
#   Host stream server connection
#   Manages Main Connection and Camera Connections
class CameraController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        # live indicator
        self.live = False
        # Mapping of camera address to camera objects
        self.cameras = {}
        # Mapping of location names to location objects
        self.locations = {}
        # Client
        self.client = None

    # Starts the controller
    def run(self):
        self.live = True
        # Start Loaded Cameras
        for address, client in self.cameras.items():
            client.start()
        self.connect()
        # Start Client Controllers Stream Connection Management
        while(self.live):
            if not self.check_connection():
                self.connect()
            time.sleep(15)

    # Stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()
        return True

    # Connect to Livestream Server
    def connect(self):
        if services.User.get_instance() is None:
            return False

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        for address, camera in self.cameras.items():
            if not camera.check_stream():
                stream = camera.start_stream()

                def loop_in_thread(loop):
                    loop.run_until_complete(stream.start())
                threading.Thread(target=loop_in_thread, args=(EVENT_LOOP,), daemon=True).start()
        return True

    # checks all rtc connections are up
    def check_connection(self):
        for address, camera in self.cameras.items():
            if not camera.check_stream():
                camera.stop_stream()
                print('Warning: Camera not connected!')
                return False
        return True

    # Loads in an Existing location
    def load_location(self, location_label):
        print('... loading location ...', location_label)
        if location_label not in self.locations:
            self.locations[location_label] = Location(location_label, self)

    # Loads in an Existing Camera
    def load_camera(self, location_label, camera_id, name, address, port, path, protocol):
        print('... loading camera ...', location_label, camera_id, name, address, port, path, protocol)
        if location_label in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location_label)
            self.cameras[address] = client
            self.locations[location_label].add_camera(client)
            self.cameras[address].start()
            self.connect()
            return client
        return None

    # Adds a new Location
    def add_location(self, location_label):
        print('... adding location ...', location_label)
        if location_label not in self.locations:
            self.locations[location_label] = Location(location_label, self)
            # TODO: Added a service function for adding a location without cameras

    # Adds a new Camera and Inserts it into database
    def add_camera(self, location_label, name, address, port, path, protocol):
        print('... adding camera ...', location_label, name, address, port, path, protocol)
        camera_id = 'c' + str(sha256((str(random.getrandbits(128))).encode('ascii')).hexdigest())
        if location_label in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location_label)
            response = services.upload_camera(client.id, client.get_metadata())
            if response is not None and response.status_code != 200:
                print('Warning: Camera not uploaded!')

            self.cameras[address] = client
            self.locations[location_label].add_camera(self.cameras[address])
            self.cameras[address].start()
            self.connect()
            return self.cameras[address]  # successfully added client

        print('Warning: Could not connect to camera', '[', camera_id, name, ']')
        return None

    def remove_location(self, location_label):
        print('... removing location ...', location_label)
        if location_label in self.locations:
            camera_ids = self.locations[location_label].cameras.keys()
            for id in camera_ids:
                self.remove_camera(id)
            del self.locations[location_label]
            return True
        return False

    def remove_camera(self, camera_id):
        print('... removing camera ...', camera_id)
        for address, camera in self.cameras.items():
            if camera.id == camera_id:
                services.remove_camera(camera.location, camera_id)
                self.locations[camera.location].remove_camera(camera_id)
                self.cameras[address].stop()
                del self.cameras[address]
                return True
        return False

    # Returns stats for a given camera address
    def client_stats(self, address):
        stats = {}
        stats['is_frames'] = self.cameras[address].stream.current_frame is not None
        stats['is_movement'] = self.cameras[address].stream.triggers.is_movement
        stats['is_person'] = self.cameras[address].stream.triggers.is_person
        stats['is_connected'] = self.cameras[address].is_connected
        return stats

    # Returns the list of cameras for a given location
    def get_cameras(self, location_label):
        cameras = []
        for id, camera in self.locations[location_label].cameras.items():
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

    def __str__(self):
        controller = 'Home Control Panel' + '\n'
        controller += '\t' + 'Site @ [label:' + site_label + ']' + '\n'
        controller += '\t' + 'Hosting [' + str(len(self.cameras)) + ' IP Camera(s)]' + '\n'
        for address, client in self.cameras.items():
            controller += '\t\t' + str(client) + '\n'
        return controller
