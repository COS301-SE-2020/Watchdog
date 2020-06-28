from app.home import HomeControlPanel
from server.server import Server
import time

def main():
    home = HomeControlPanel(Server("127.0.0.1"))
    # home.add_camera('10.0.0.105', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')
    for x in range(3):
        home.add_camera('data/sample/big_chungus.mp4')
    for x in range(3):
        home.add_camera('data/sample/still_grey.mp4')
    for x in range(3):
        home.add_camera('data/sample/big_chungus.mp4')
    for x in range(3):
        home.add_camera('data/sample/still_grey.mp4')

    home.start()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
