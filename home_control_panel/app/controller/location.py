
class Location:
    def __init__(self, location, controller):
        self.label = location
        self.controller = controller
        self.cameras = {}

    def add_camera(self, camera):
        self.cameras[camera.address] = camera

    def get_metadata(self):
        camera_list = ''
        for index in range(len(self.cameras)):
            camera_list += str(self.cameras.id)
        return {
            "location": self.label,
            "cameras": camera_list
        }
