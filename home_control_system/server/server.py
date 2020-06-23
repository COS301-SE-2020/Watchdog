import cv2
from imutils import build_montages
from .camera import Camera


class Server:
    def __init__(self, address, location='Home'):
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
            client.connect(protocol)
            if client.is_connected:
                self.cameras[address] = client
            return True  # successfully added client
        return False

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
    def run(self, display=True):
        if self.cameras.__len__() == 0:
            print("Error: There are currently no ip cameras detected.")

        self.live = True
        client_frames = {}
        for address, client in self.cameras.items():
            if not display:
                client.output = False
            client.set_frame(self.height / len(self.cameras), self.width / len(self.cameras))
            client.start()

        while self.live:
            try:
                if display:
                    for address, client in self.cameras.items():
                        if client.current_frame is not None:
                            client_frames[address] = client.current_frame
                    montages = build_montages(client_frames.values(), (self.width, self.height), (len(self.cameras), 1))
                    for (i, montage) in enumerate(montages):
                        cv2.imshow("Montage Footage {}".format(i), montage)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            except KeyboardInterrupt:
                break

        for address, client in self.cameras.items():
            client.stop()
            client.disconnect()

        # close output window
        cv2.destroyAllWindows()

    def client_stats(self, address):
        stats = {}
        stats['is_connected'] = self.cameras[address].is_connected
        stats['is_movement'] = self.cameras[address].is_movement
        stats['is_person'] = self.cameras[address].is_person
        stats['is_frames'] = self.cameras[address].current_frame is not None
        return stats
