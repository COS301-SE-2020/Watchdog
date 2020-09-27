import os
from PyQt5.QtWidgets import QApplication
from ..service.settings import Settings
from .controller.controller import CameraController


class ControlPanel(QApplication):
    def __init__(self):
        super(ControlPanel, self).__init__([])
        self.setup()
        self.setApplicationName("Watchdog Control Panel")
        self.settings = Settings()
        self.controller = CameraController(self)

    def start(self):
        self.exec_()

    def end(self):
        self.controller.stop()
        self.controller.join()
        os._exit(1)

    def add_location(self, location_label):
        # simply add a new location
        pass

    def add_camera(self, location_label, camera_id, name, address, port, path, protocol):
        # simply add the camera to the UI for a given location label
        pass

    def repair_camera(self, location_label, camera_id, name, address, port, path, protocol):
        # ask user to enter a new camera with the given details in the fields for editing
        pass

    def attach_stream(self, camera_id, stream_object):
        stream_view = None  # TODO: find ui component for given camera_id
        stream_object.set_view(stream_view)  # this will now automatically call : stream_view.update(current_frame); when a new frame is grabbed

    @staticmethod
    def setup():
        # Directory Structure
        if not os.path.exists('data'):
            os.mkdir('data')
        if not os.path.exists('data/temp'):
            os.mkdir('data/temp')
        if not os.path.exists('data/temp/video'):
            os.mkdir('data/temp/video')
        if not os.path.exists('data/temp/image'):
            os.mkdir('data/temp/image')
        # Utility Files
        if not os.path.exists('data/.conf'):
            with open('data/.conf', 'w'):
                pass
        if not os.path.exists('data/.hash'):
            with open('data/.hash', 'w'):
                pass
        if not os.path.exists('data/.logs'):
            with open('data/.logs', 'w'):
                pass
