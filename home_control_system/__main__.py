from app.home import HomeControlPanel
from server.server import Server
from service.services import upload_to_s3


def main():
    home = HomeControlPanel(Server('127.0.0.1'))
    # home.add_camera('10.0.0.105', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')
    for x in range(4):
        home.add_camera('data/sample/surveillance1.mp4')
        home.add_camera('data/sample/surveillance2.mp4')
    home.start()


def detect_intruder_integration():
    path = "data/temp/images"
    file_name = "test.jpeg"
    tag = "detected"
    response = upload_to_s3(path, file_name, tag)
    print(response)


if __name__ == "__main__":
    print("Running Home Control Panel")
    # main()
    detect_intruder_integration()
