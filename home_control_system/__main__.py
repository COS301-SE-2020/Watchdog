from app.home import HomeControlPanel
from server.server import Server


def main():
    home = HomeControlPanel(Server('127.0.0.1', 'Home', 5000))
    home.add_camera('10.0.0.105', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')  # Android IP Camera App
    for x in range(4):
        home.add_camera('data/sample/surveillance1.mp4')  # Sample CCTV Clips
        home.add_camera('data/sample/surveillance2.mp4')  # Sample CCTV Clips
    home.start()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
