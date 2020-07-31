import time
import threading
from service import services
from ..component import Component


class Location:
    count = 0

    def __init__(self, location):
        self.id = Location.count
        self.label = location
        self.cameras = []
        Location.count += 1

    def add_camera(self, camera_id, address, port='', path='', protocol=''):
        camera = Component.root.controller.add_camera(camera_id, address, port, path, self.label, protocol)
        if camera is not None:
            self.cameras.append(camera)
        return camera

    def get_metadata(self):
        camera_list = ''
        for index in range(len(self.cameras)):
            camera_list += str(self.cameras.id)
        return {
            "location": self.label,
            "cameras": camera_list
        }


class LocationList(threading.Thread):
    def __init__(self, view=None):
        threading.Thread.__init__(self)
        self.locations = []
        self.view = view
        self.index = 0

    def run(self):
        while(True):
            self.view.home.view.grid.viewer.refresh()
            time.sleep(1 / 30)  # 30 fps

    def add_location(self, label):
        location = Location(label)

        self.index = Location.count

        self.locations.append(location)

        if self.view is not None:
            self.view.home.sidepanel.list.add_button(label)

        return location

    def add_camera(self, camera_id, address, port='', path='', protocol='', upload=True, index=None):
        if self.index > len(self.locations) - 1:
            return None

        if index is not None:
            self.index = index

        camera = self.locations[self.index].add_camera(
            camera_id,
            address,
            port,
            path,
            protocol
        )

        if camera is not None and camera.is_connected:
            if self.view is not None:
                self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)

            if upload:
                response = services.upload_camera(camera.id, camera.get_metadata())
                if response is not None and response.status_code != 200:
                    return None

            return camera
        return None

    def changeActive(self, index):
        self.index = index
        self.view.home.view.grid.set_stream_views(self.locations[self.index].cameras)
