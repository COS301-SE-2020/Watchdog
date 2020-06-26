from app.home import HomeControlPanel
from server.server import Server


def main():
    home = HomeControlPanel(Server("127.0.0.1"))
    home.add_camera('10.0.0.117', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')
    home.add_camera('10.0.0.106', '8080', 'h264_ulaw.sdp', 'Tablet Camera', 'rtsp')
    home.add_camera('data/sample/big_chungus.mp4')
    home.add_camera('data/sample/still_grey.mp4')
    home.start()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
