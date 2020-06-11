from time import sleep
import pytest
from vidgear.gears import NetGear
import cv2 as cv
from threading import Thread
from home_controller_system.server import Server


def send_frame_to_server(port):

    stream = cv.VideoCapture("test_video/big_buck_bunny_720p_1mb.mp4")
    options = {"multiserver_mode": True}
    server = NetGear(
        address="127.0.0.1", port=port, protocol="tcp", pattern=1, **options
    )
    try:
        (grabbed, frame) = stream.read()
        if not grabbed:
            raise Exception(
                "Could not send video frame image. Please check that your video path is correct!"
            )
        server.send(frame)
    except Exception as e:
        print(e)

    stream.release()
    server.close()


def test_successfully_add_client():
    server = Server("127.0.0.1")
    response = server.add_client(5566)

    assert server.is_client_connected(5566) is True
    assert response is 200


def test_adding_client_with_same_port_number():
    server = Server("127.0.0.1")
    response = server.add_client(5566)
    response2 = server.add_client(5566)

    assert response == 200
    assert response2 == 501


def test_successfully_add_clients():
    server = Server("127.0.0.1")
    response = server.add_client(5566)
    server.add_client(5567)
    server.add_client(5568)

    assert server.num_of_cameras == 3
    assert server.is_client_connected(5566) is True
    assert server.is_client_connected(5567) is True
    assert server.is_client_connected(5568) is True
    assert response is 200


def test_server_receives_frames():
    server = Server("127.0.0.1")
    server.add_client(5566)

    p1 = Thread(target=server.run, args=(False,))
    p1.start()
    sleep(2)
    p2 = Thread(target=send_frame_to_server, args=(5566,))
    p2.start()
    sleep(2)
    response = server.did_client_send_frame(5566)

    assert response is True
