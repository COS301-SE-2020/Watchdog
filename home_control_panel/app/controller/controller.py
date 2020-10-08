import asyncio
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
from ...service import rtc_connection

import nest_asyncio
nest_asyncio.apply()

conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']

EVENT_LOOP = asyncio.get_event_loop()
asyncio.set_event_loop(EVENT_LOOP)


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
        self.camera_producers = {}

    # Starts the controller
    def run(self):
        if self.cameras.__len__() == 0:
            print("There are currently no ip cameras detected...")
        self.live = True
        # Start Loaded Cameras
        for address, client in self.cameras.items():
            client.start()
        # Start Client Controllers Stream Connection Management
        # while(self.live):
            # pass
            # self.check_connection()
            # for address, client in self.cameras.items():
            #     if not client.check_connection():
            #         client.connect()
            # time.sleep(5)
        self.connect([key for key in self.cameras])

    # Stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()
        # self.client.socket.disconnect()
        return True

    # Connect to Livestream Server
    def connect(self, camera_ids, camera_addresses:list=None):
        # if services.User.get_instance() is None:
        #     return False
        # if self.client is None and services.User.get_instance().hcp_id is not None:
        #     # self.client = connection.Producer(services.User.get_instance().user_id, services.User.get_instance().hcp_id, self)
        #     self.client = rtc_connection.RTCConnectionHandler(user_id=services.User.get_instance().user_id, camera_id=)
        # if self.client is not None and not self.client.connected:
        #     exp_wait = 1
        #     while not self.client.connect():
        #         time.sleep(exp_wait ^ exp_wait)
        #         exp_wait += 1
        #         if exp_wait > 6:
        #             return False
        # if self.client is not None:
        #     self.client.authorize()
        if camera_addresses is not None:
            for i, camera_id in enumerate(camera_ids):
                self.camera_producers[camera_id] = rtc_connection.RTCConnectionHandler(
                    camera_id,
                    services.User.get_instance().user_id,
                    camera_addresses[i]
                )

                def loop_in_thread(loop):
                    loop.run_until_complete(self.camera_producers[camera_id].start())
                # asyncio.run(self.camera_producers[camera_id].start())

                threading.Thread(target=loop_in_thread, args=(EVENT_LOOP,), daemon=True).start()

        return True

    # def check_connection(self):
    #     if self.client is None or not self.client.connected:
    #         return self.connect()
    #
    #     if self.client is not None:
    #         self.client.pulse(True)
    #
    #     return self.client.connected

    # Starts the given cameras livestreams, stops all the others
    # def start_streams(self, camera_list):
        # if self.check_connection():
        #     for address, camera in self.cameras.items():
        #         if camera.id in camera_list:
        #             camera.start_stream(self.client)
        #         else:
        #             camera.stop_stream()
        # else:
        #     self.stop_streams()

    # Stops all camera streams
    # def stop_streams(self):
    #     for address, camera in self.cameras.items():
    #         camera.stop_stream()

    # Loads in an Existing location
    def load_location(self, location_label):
        print('LOADING LOCATION', location_label)
        if location_label not in self.locations:
            self.locations[location_label] = Location(location_label, self)

    # Loads in an Existing Camera
    def load_camera(self, location_label, camera_id, name, address, port, path, protocol):
        print('LOADING CAMERA', location_label, camera_id, name, address, port, path, protocol)
        if location_label in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location_label)
            if client.is_connected:
                print("Loading camera " + str(client))
                self.cameras[address] = client
                self.locations[location_label].add_camera(client)
                self.cameras[address].start()
                self.connect([camera_id], [protocol+'://'+str(client.get_url())])
                return client
        return None

    # Adds a new Location
    def add_location(self, location_label):
        print('ADDING LOCATION', location_label)
        if location_label not in self.locations:
            self.locations[location_label] = Location(location_label, self)
            # TODO: Added a service function for adding a location without cameras

    # Adds a new Camera and Inserts it into database
    def add_camera(self, location_label, name, address, port, path, protocol):
        print('ADDING CAMERA', location_label, name, address, port, path, protocol)
        camera_id = 'c' + str(sha256((str(random.getrandbits(128))).encode('ascii')).hexdigest())
        if location_label in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location_label)
            print("Adding camera " + str(client))
            if client.is_connected:
                response = services.upload_camera(client.id, client.get_metadata())
                if response is not None and response.status_code != 200:
                    print('Warning: Camera not uploaded!')

                self.cameras[address] = client
                self.locations[location_label].add_camera(self.cameras[address])
                # if self.check_connection():
                #     self.client.authorize()

                self.cameras[address].start()
                self.connect([camera_id])
                return self.cameras[address]  # successfully added client
            else:
                print('Warning: Could not connect to camera', '[', camera_id, name, ']')
        return None

    def remove_location(self, location_label):
        print('REMOVING LOCATION', location_label)
        if location_label in self.locations:
            camera_ids = self.locations[location_label].cameras.keys()
            for id in camera_ids:
                self.remove_camera(id)
            del self.locations[location_label]
            return True
        return False

    def remove_camera(self, camera_id):
        print('REMOVING CAMERA', camera_id)
        for address, camera in self.cameras.items():
            if camera.id == camera_id:
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
