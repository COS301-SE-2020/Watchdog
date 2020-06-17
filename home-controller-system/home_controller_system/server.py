import cv2
from vidgear.gears import NetGear
from imutils import build_montages
from home_controller_system.connector import Connector

class Server:
    def __init__(self, address, location = 'Home'):
        self.address = address
        self.location = location
        self.clients = {}
        self.cam_count = 0
        self.live = False
        self.height = 720
        self.width = 1080

    # adds a ip camera client to an allocated port on the server
    def add_camera(self, address, location = 'Room', is_IP = True):
        if not self.check_address(address):
            print("Adding camera " + address + " - " + location)
            client = Connector(address, location)
            if is_IP:
                protocol = 'rtsp://'
            else:
                protocol = ''
            client.connect(protocol)
            if client.is_connected:
                self.clients[address] = client
                self.cam_count += 1
            return True  # successfully added client
        return False

    def check_address(self, address):
        # quick check
        if f"{self.address}" in self.clients: 
            return True
        # double check
        # for camera_client in self.clients:
        for camera_address, camera_client in self.clients.items():
            if camera_client.address == address:
                return True
        return False

    # starts the server
    def run(self, display = True):
        if self.clients.__len__() == 0:
            print("Error: There are currently no ip cameras detected.")
        
        self.live = True
        client_frames = {}
        for address, client in self.clients.items():
            if not display:
                client.output = False
            client.frame(self.height / self.cam_count, self.width / self.cam_count)
            client.start()

        while self.live:
            try:
                if display:
                    for address, client in self.clients.items():
                        if client.current_frame is not None:
                            client_frames[address] = client.current_frame
                    montages = build_montages(client_frames.values(), (self.width, self.height), (self.cam_count, 1))
                    for (i, montage) in enumerate(montages):
                        cv2.imshow("Montage Footage {}".format(i), montage)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

            except KeyboardInterrupt:
                break

        for address, client in self.clients.items():
            client.stop()
            client.disconnect()
        
        # close output window
        cv2.destroyAllWindows()

    def client_stats(self, address):
        stats = {}
        stats['is_connected'] = self.clients[address].is_connected
        stats['is_movement'] = self.clients[address].is_movement
        stats['is_person'] = self.clients[address].is_person
        stats['is_frames'] = self.clients[address].current_frame is not None
        return stats

def main():
    server = Server("127.0.0.1")
    # server.add_camera('10.0.0.109:8080/h264_ulaw.sdp', 'Phone Camera')
    # server.add_camera('10.0.0.110:8080/h264_ulaw.sdp', 'Tablet Camera', True)
    server.add_camera('tests/test_video/big_chungus.mp4', 'Video', False)
    server.run()
