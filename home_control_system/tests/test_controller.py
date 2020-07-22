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
    response = controller.add_camera(address, '', '', 'Video', '')
    stats = controller.client_stats(address)

    assert response is not None
    assert stats['is_connected'] is True


def test_test_add_client_same_address():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    response1 = controller.add_camera(address, '', '', 'Video', '')
    response2 = controller.add_camera(address, '', '', 'Video', '')

    assert response1 is not None
    assert response2 is None


def test_add_clients():
    controller = CameraController()

    address1 = 'data/sample/big_chungus.mp4'
    response1 = controller.add_camera(address1, '', '', 'Video', '')
    stats1 = controller.client_stats(address1)

    address2 = 'data/sample/still_grey.mp4'
    response2 = controller.add_camera(address2, '', '', 'Video', '')
    stats2 = controller.client_stats(address2)

    assert response1 is not None
    assert response2 is not None
    assert len(controller.cameras) == 2
    assert stats1['is_connected'] is True
    assert stats2['is_connected'] is True


def test_controller_receives_frames():
    controller = CameraController()
    address = 'data/sample/big_chungus.mp4'
    response = controller.add_camera(address, '', '', 'Video', '')

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
    response = controller.add_camera(address, '', '', 'Video', '')

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
    response = controller.add_camera(address, '', '', 'Video', '')

    controller.run()
    sleep(1.5)
    stats = controller.client_stats(address)
    controller.stop()

    stats = controller.client_stats(address)

    assert response is not None
    assert stats['is_movement'] is True
