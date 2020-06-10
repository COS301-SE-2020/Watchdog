from vidgear.gears import NetGear
import cv2

# Open suitable video stream (webcam on first index in our case)
stream = cv2.VideoCapture(0)

# activate multiserver_mode
# options = {'multiserver_mode': True, 'secure_mode': 1, "overwrite_cert": True}
options = {'multiserver_mode': True}
server = NetGear(address='127.0.0.1', port='5566', protocol='tcp', pattern=1, **options)

# loop over until Keyboard Interrupted
while True:
    try:
        # read frames from stream
        (grabbed, frame) = stream.read()

        # check for frame if not grabbed
        if not grabbed:
            break

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        break

# safely close video stream
stream.release()

# safely close server
server.close()
