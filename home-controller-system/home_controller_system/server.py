from time import sleep
from vidgear.gears import NetGear
import imutils
import os
import cv2 as cv
import numpy as np
import copy

# multi server connecting to one client.
# secure tcp connection between client & server with StoneHouse; overwrite encryption key each time connection is made


class Client:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.surface = 0

        self.moving_average = None
        self.difference = None
        self.temp = None

    def identify_movement(self, current_frame, ceil):
        grey = cv.cvtColor(copy.deepcopy(current_frame), cv.COLOR_BGR2GRAY)  # convert frame to grey -> 1 vs 3 channel
        grey = cv.GaussianBlur(grey, (21, 21), 0)

        if self.moving_average is None:
            self.moving_average = np.float32(copy.deepcopy(current_frame))

        if self.difference is None:
            self.difference = copy.deepcopy(current_frame)
            self.temp = copy.deepcopy(current_frame)
            cv.convertScaleAbs(current_frame, self.moving_average, 1.0, 0.0)
        else:
            cv.accumulateWeighted(current_frame, self.moving_average, 0.020, None)  # Compute the average

        cv.convertScaleAbs(self.moving_average, self.temp, 1.0, 0.0)
        self.difference = cv.absdiff(current_frame, self.temp)

        self.difference = grey
        threshold = cv.threshold(self.difference, 25, 255, cv.THRESH_BINARY)[1]
        threshold = cv.dilate(threshold, None, iterations=2)  # fill in the holes

        contours = cv.findContours(threshold.copy(), cv.RETR_EXTERNAL,  # find the contours
                                   cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        current_surface_area = 0
        for c in contours:
            current_surface_area += cv.contourArea(c)

        avg = (current_surface_area * 100)  # calculating the average of contour area on the total size
        if avg > ceil:
            return True
        return False

    def __str__(self):
        return f"{self.ip_address}:{self.port}"


class Server:
    def __init__(self, num_of_cameras, ip_address, ceil=15):
        try:
            self.num_of_cameras = num_of_cameras
            self.ip_address = ip_address
            self.clients = {}
            self.ceil = ceil
            if not self.is_connected_to_internet():
                raise Exception(" Could not connect to the internet!")
        except Exception as e:
            print(e)

    def add_client(self, port):
        if self.ip_address is not None:
            is_valid = True
            for client in self.clients:
                if client.port != port:
                    is_valid = False
            if is_valid:
                client = Client(self.ip_address, port)
                self.clients[client.__str__()] = client
                return 200  # successfully added client
            else:
                return 401  # client already exists
        return 500  # server does not have an ip_address

    def is_connected_to_internet(self):
        if self.ip_address:
            if os.system(f"ping -o -c 3 -W 3000 {self.ip_address}") != 0:
                return 200  # server is connected to the given ip address
        return 500

    def is_client_connected(self, port):
        if f"{self.ip_address}:{port}" in self.clients:  # if client is connected -> client __str__ is in dictionary
            return True
        return False

    def run(self):
        ports = []

        if self.clients.__sizeof__() > 0:
            for client in self.clients:
                p = self.clients.get(client)
                ports.append(p.port)
        else:
            print("There are currently no ip cameras detected!")
            return 500

        # options = {'multiserver_mode': True, 'secure_mode': 1, "overwrite_cert": True}
        options = {'multiserver_mode': True}
        netgear = NetGear(address='127.0.0.1', port=ports, protocol='tcp', pattern=1, receive_mode=True, **options)
        # loop over
        while True:
            try:
                # read frames from stream
                frame = netgear.recv()
                if frame is None:
                    print("could not connect to your ip camera")
                    break

                port, frame = frame
                if self.is_client_connected(port):
                    current_client = self.clients[f"{self.ip_address}:{port}"]
                    if current_client.identify_movement(copy.deepcopy(frame), self.ceil):
                        print("Something is moving!")
                        sleep(2)
                        # send frame to intruder detection module
                cv.imshow("Live Steam", frame)
            except KeyboardInterrupt:
                "Keyboard interrupt!"
                break
        cv.destroyAllWindows()
        netgear.close()


if __name__ == "__main__":
    server = Server(2, '127.0.0.1')
    server.add_client('5566')
    server.run()
