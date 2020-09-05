from time import sleep
from threading import Thread
from service import config
from app.controller.controller import CameraController


# UNIT-TESTS
#   1 -- test_add_client
#   2 -- test_test_add_client_same_address
#   3 -- test_add_clients
#   4 -- test_controller_receives_frames
#   5 -- test_frames_without_movement
#   6 -- test_frames_with_movement


def test_add_client():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    controller.add_location('x')
    response = controller.load_camera('x', 'q', address, '', '', '')
    stats = controller.client_stats(address)

    print(response)
    print(stats)

    assert response is not None
    assert stats['is_connected'] is True


def test_test_add_client_same_address():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    controller.add_location('x')
    response1 = controller.load_camera('x', 'q', address, '', '', '')
    response2 = controller.load_camera('x', 'q', address, '', '', '')

    assert response1 is not None
    assert response2 is None


def test_add_clients():
    controller = CameraController()

    controller.add_location('x')

    address1 = 'data/sample/big_chungus.mp4'
    response1 = controller.load_camera('x', 'q', address1, '', '', '')
    stats1 = controller.client_stats(address1)

    address2 = 'data/sample/still_grey.mp4'
    response2 = controller.load_camera('x', 'q', address2, '', '', '')
    stats2 = controller.client_stats(address2)

    assert response1 is not None
    assert response2 is not None
    assert len(controller.cameras) == 2
    assert stats1['is_connected'] is True
    assert stats2['is_connected'] is True


def test_controller_receives_frames():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    controller.add_location('x')
    response = controller.load_camera('x', 'q', address, '', '', '')

    controller.run()
    sleep(0.5)
    stats = controller.client_stats(address)
    controller.stop()

    assert response is not None
    assert controller.cameras[address].stream.current_frame is not None
    assert stats['is_frames'] is True


def test_frames_without_movement():
    controller = CameraController()
    address = 'data/sample/still_grey.mp4'
    controller.add_location('x')
    response = controller.load_camera('x', 'q', address, '', '', '')

    controller.run()
    sleep(0.5)
    stats = controller.client_stats(address)
    controller.stop()

    stats = controller.client_stats(address)

    assert response is not None
    assert stats['is_movement'] is False


def test_frames_with_movement():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    controller.add_location('x')
    response = controller.load_camera('x', 'q', address, '', '', '')

    controller.run()
    sleep(1.5)
    stats = controller.client_stats(address)
    controller.stop()

    stats = controller.client_stats(address)

    assert response is not None
    assert stats['is_movement'] is True
