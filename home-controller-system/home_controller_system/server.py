from vidgear.gears import NetGear
from imutils import build_montages, grab_contours
import cv2
import numpy as np


class Client:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        self.received_frame = False
        self.current_frame = None

        self.is_movement = False
        self.moving_average = None
        self.difference = None
        self.temp = None

    def __str__(self):
        return f"{self.ip_address}:{self.port}"

    def identify_movement(self, cf, ceil):
        grey = cv2.cvtColor(
            cf, cv2.COLOR_BGR2GRAY
        )  # convert frame to grey -> 1 vs 3 channel
        grey = cv2.GaussianBlur(grey, (21, 21), 0)
        grey = np.array(grey, dtype=np.uint8)

        if self.moving_average is None:
            self.moving_average = np.array(cf, dtype=float)

        if self.difference is None:
            self.difference = cf
            self.temp = cf
            cv2.convertScaleAbs(cf, self.moving_average, 1.0, 0.0)
        else:
            cv2.accumulateWeighted(cf, self.moving_average, 0.020, None)

        cv2.convertScaleAbs(self.moving_average, self.temp, 1.0, 0.0)
        self.difference = cv2.absdiff(cf, self.temp)

        self.difference = cv2.cvtColor(self.difference, cv2.COLOR_BGR2GRAY)
        threshold = cv2.threshold(self.difference, 70, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=18)  # fill in the holes
        threshold = cv2.erode(threshold, None, iterations=10)

        contours = cv2.findContours(
            threshold.copy(),
            cv2.RETR_EXTERNAL,  # find the contours
            cv2.CHAIN_APPROX_SIMPLE,
        )
        contours = grab_contours(contours)
        back_contours = contours  # Save contours
        current_surface_area = 0
        for c in contours:
            current_surface_area += cv2.contourArea(c)

        avg = (
            current_surface_area * 100
        )  # calculating the average of contour area on the total size
        cv2.drawContours(self.current_frame, back_contours, -1, (0, 255, 0), 1)

        if avg > ceil:
            self.is_movement = True
            return True
        return False


class Server:
    def __init__(self, ip_address, ceil=15):
        self.ip_address = ip_address
        self.ceil = ceil

        self.clients = {}
        self.num_of_cameras = 0

    def add_client(self, port):
        is_valid = False
        if self.ip_address is not None:
            if self.clients.__len__() > 0:
                for c in self.clients:
                    if self.clients[c].port != port:
                        is_valid = True
            else:
                is_valid = True

        if is_valid:
            client = Client(self.ip_address, port)
            self.clients[client.__str__()] = client
            self.num_of_cameras += 1
            return 200  # successfully added client
        else:
            return 501

    def build_montage(self, frames, width, height):
        montages = build_montages(
            frames.values(), (width, height), (self.num_of_cameras, 1)
        )

        for (i, montage) in enumerate(montages):
            cv2.imshow("Montage Footage {}".format(i), montage)

    def is_client_connected(self, port):
        if (
            f"{self.ip_address}:{port}" in self.clients
        ):  # if client is connected -> client __str__ is in dictionary
            # client = self.clients[f"{self.ip_address}:{port}"]
            return True
        return False

    def get_current_client_frames(self):
        cf = {}
        for c in self.clients:
            temp = self.clients.get(c)
            if temp.current_frame is not None:
                cf[temp.__str__()] = temp.current_frame
        return cf

    def did_client_send_frame(self, port):
        return self.clients[f"{self.ip_address}:{port}"].received_frame

    def run(self, display_video=True):
        ports = []
        if self.clients.__len__() > 0:
            for c in self.clients:
                ports.append(self.clients[c].port)
        else:
            print("There are currently no ip cameras detected!")
            return 500
        # activate multiserver_mode
        options = {"multiserver_mode": True}

        client = NetGear(
            address=self.ip_address,
            port=ports,
            protocol="tcp",
            pattern=1,
            receive_mode=True,
            **options,
        )
        while True:
            try:
                # receive data from network
                data = client.recv()
                # check if data received isn't None
                if data is None:
                    break
                # extract unique port address and its respective frame
                unique_address, frame = data

                # get extracted frame's shape
                if self.is_client_connected(unique_address):
                    current_client = self.clients[f"{self.ip_address}:{unique_address}"]
                    current_client.received_frame = True
                    current_client.current_frame = frame
                    if current_client.identify_movement(frame, self.ceil):
                        print("Something is moving!")

                if display_video:
                    frame_dict = self.get_current_client_frames()
                    # build a montage using data dictionary
                    (h, w) = frame.shape[:2]
                    self.build_montage(frame_dict, w, h)

            except KeyboardInterrupt:
                break
        # close output window
        cv2.destroyAllWindows()

        # safely close client
        client.close()


if __name__ == "__main__":
    server = Server("127.0.0.1")
    server.add_client(5566)
    # server.add_client(5567)
    server.run()
