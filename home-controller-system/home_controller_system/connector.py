import cv2
import time
import threading
import numpy as np
import pandas as pd
from imutils import grab_contours

class Connector(threading.Thread):
    def __init__(self, address, location, height=480, width=360):
        threading.Thread.__init__(self)
        self.live = False
        self.protocol = ''
        self.address = address
        self.location = location
        self.output = True
        self.is_connected = False
        self.is_movement = False
        self.is_person = False
        self.current_frame = None # set in server class
        self.moving_average = None
        self.cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.height = height
        self.width = width

    def run(self):
        print("Starting Camera Client [" + self.address + "] Location:" + self.location)
        self.live = True
        while(True):
            if not self.live:
                return
            self.update()

    def stop(self):
        self.live = False

    def frame(self, height, width):
        self.height = int(height)
        self.width = int(width)

    def connect(self, protocol):
        self.protocol = protocol
        self.stream = cv2.VideoCapture(self.protocol + self.address)
        if self.stream.isOpened():
            print("Connected to IP Camera [" + self.address + "]")
            self.is_connected = True
        else:
            print("Failed to connect to IP Camera [" + self.address + "]")
            self.is_connected = False

    def disconnect(self):
        self.stream.release()
        self.is_connected = False 

    def update(self, frame_analysis = True):
        if(not self.is_connected):
            self.connect(self.protocol)

        fps = 60
        limit = 1000 / fps #milliseconds
        begin = time_now()

        (grabbed, frame) = self.stream.read()
        # check for frame if not grabbed
        if grabbed:
            # self.current_frame = frame
            self.current_frame = cv2.resize(frame, (self.width, self.height))
            if(frame_analysis):
                self.detect_movement(self.current_frame)
                if self.is_movement:
                    self.detect_faces(self.current_frame)
                    if self.output:
                        if self.is_person:
                            print("Someone is present!")
                        else:
                            print("Movement detected!")
        else:
            self.is_connected = False 

        now = time_now()
        while now < begin + limit:
            now = time_now()                   

    def detect_movement(self, cf, ceil = 15):
        if self.moving_average is None:
            self.moving_average = np.array(cf, dtype=float)
        cv2.accumulateWeighted(cf, self.moving_average, 0.05) # add to moving average
        background = cv2.convertScaleAbs(self.moving_average)
        difference = cv2.cvtColor(cv2.absdiff(cf, background), cv2.COLOR_BGR2GRAY)

        threshold = cv2.threshold(difference, 70, 255, cv2.THRESH_BINARY)[1]
        threshold = cv2.dilate(threshold, None, iterations=2)  # fill in the holes
        threshold = cv2.erode(threshold, None, iterations=1)

        contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = grab_contours(contours)
        current_surface_area = 0
        for c in contours:
            current_surface_area += cv2.contourArea(c)

        avg = current_surface_area * 100 # calculating the average of contour area on the total size
        cv2.drawContours(self.current_frame, contours, -1, (0, 255, 0), 1)

        self.is_movement = False
        if avg > ceil:
            self.is_movement = True

        return self.is_movement

    def detect_faces(self, cf, scaleFactor = 1.1):
        grey = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2GRAY)
        faces_rect = self.cascade.detectMultiScale(grey, scaleFactor=scaleFactor, minNeighbors=5) # applying the haar classifier to detect faces
        self.is_person = False

        for (x, y, w, h) in faces_rect:
            cv2.rectangle(self.current_frame, (x, y), (x+w, y+h), (0, 255, 0), 15)
            self.is_person = True

        return self.is_person


def time_now():
    return int(round(time.time() * 1000))