import os
import time
import json
import random
import threading
from hashlib import sha256
from ...service import services
from ...service import connection
from .camera import Camera
from .location import Location
from ...cli import debug

conf = json.loads(os.environ['config'])
site_label = conf['settings']['site']


class CameraController(threading.Thread):
    def __init__(self, app=None):
        debug('Init Camera Controller...')
        threading.Thread.__init__(self)
        self.client = None
        self.live = False
        self.locations = {}
        self.cameras = {}
        self.app = app
        debug('DONE Init Camera Controller')

    # Called at Start, Pass in UI Window for UI Setup
    def setup_environment(self):
        print('Loading Environment...')
        locations = services.get_camera_setup()

        debug('Locations Loaded')
        debug(locations, header='Printing Locations', footer='Done Print Locations')

        if locations is not None:
            debug('Locations not None...\n Loading cameras...')
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
                            if self.app is not None:
                                self.app.window.fix_camera(camera['name'], camera['address'], camera['port'], camera['protocol'], camera['path'])
                            services.remove_camera(location, camera_id)
            self.update_widgets()
            debug('Done Loading Environment (Returning True)')
            return True
        debug('Done Loading Environment (Returning False)')
        return False

    def update_widgets(self):
        debug('Camera Controller: Updating Widgets...')
        if self.app is not None:
            debug('Camera Controller: App is not None...')
            self.app.window.set_locations(self.get_locations())
            self.app.window.set_cameras(self.get_cameras(location=self.app.current_location))
        debug('Camera Controller: App is None...')

    def get_cameras(self, location):
        debug('CameraController: Getting Cameras...')
        cameras = []
        for address, camera in self.locations[location].cameras.items():
            cameras.append(camera)
        debug('CameraController: DONE Getting Cameras')
        return cameras

    def get_locations(self):
        debug('CameraController: Getting Locations...')
        locations = []
        for location, location_object in self.locations.items():
            locations.append(location)
        debug('CameraController: DONE Getting Locations')
        return locations

    def load_location(self, label):
        debug('CameraController: Loading Locations...')
        if label not in self.locations:
            debug('CameraController: \tLocation not in locations. Creating New Location in App Location...')
            self.locations[label] = Location(label, self)
            if self.app.current_location == '':
                debug('CameraController: \tCurrent App Location Blank. Changing Location...')
                self.app.change_location(label)
        debug('CameraController: DONE Loading Locations')

    def add_location(self, label):
        debug(f'CameraController: adding location {label}...')
        if label not in self.locations:
            debug('CameraController: putting in dict...')
            self.locations[label] = Location(label, self)
            if self.app is not None:
                debug('CameraController: \tCurrent App Location Blank. Changing Location...')
                self.app.change_location(label)
            self.update_widgets()
        debug('CameraController: DONE Adding Location')

    def load_camera(self, location, camera_id, name, address, port, path, protocol):
        debug(f'CameraController: Loading Camera {location} => {name} => {camera_id}')
        if location in self.locations and address not in self.cameras:
            client = Camera(camera_id, protocol, name, address, port, path, location)
            if client.is_connected:
                print("Loading camera " + str(client))
                self.cameras[address] = client
                self.locations[location].add_camera(client)
                return client  # successfully added client
        return None

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
                self.locations[location].add_camera(self.cameras[address])
                self.client.add_camera(self.cameras[address].id)
                self.cameras[address].start()

                self.update_widgets()
                return client  # successfully added client
        return None

    # starts the controller
    def run(self):
        debug('Camera Controller: Running....')
        self.live = True
        if self.cameras.__len__() == 0:
            print("There are currently no ip cameras detected...")

        for address, client in self.cameras.items():
            client.start()

        camera_ids = []

        for address, camera in self.cameras.items():
            camera_ids.append(camera.id)

        if self.app is not None:
            user_id = services.User.get_instance().user_id
            producer_id = services.User.get_instance().hcp_id
            self.client = connection.Producer(user_id, producer_id, camera_ids, self)
            while(True):
                self.app.window.home.view.grid.viewer.refresh()
                # self.app.window.home.view.grid.retriever.refresh()
                time.sleep(1 / 30)

    # stops the controller
    def stop(self):
        self.live = False
        for address, client in self.cameras.items():
            client.stop()
            client.join()

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
