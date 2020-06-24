from server.server import Server

def main():
    serve = Server("127.0.0.1")
    # serve.add_camera('10.0.0.114', '8080', 'h264_ulaw.sdp', 'Phone Camera', 'rtsp')
    serve.add_camera('data/sample/big_chungus.mp4', '', '', '', '')
    serve.run()


if __name__ == "__main__":
    print("Running Home Control Panel")
    main()
