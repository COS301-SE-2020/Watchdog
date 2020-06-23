from server.server import Server

def main():
    serve = Server("127.0.0.1")
    serve.add_camera('10.0.0.109', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')
    # server.add_camera('10.0.0.110', '8080', 'h264_ulaw.sdp', 'Tablet Camera', 'rtsp')
    # server.add_camera('data/big_chungus.mp4', 'Video', '')
    serve.run()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
