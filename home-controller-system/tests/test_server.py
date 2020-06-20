from time import sleep
import pytest
from vidgear.gears import NetGear
import cv2 as cv
from threading import Thread
from home_controller_system.server import Server


# UNIT-TESTS
#   1 -- test_add_client
#   2 -- test_test_add_client_same_address
#   3 -- test_add_clients
#   4 -- test_server_receives_frames
#   5 -- test_frames_without_movement
#   6 -- test_frames_with_movement


def test_add_client():
    server = Server('127.0.0.1')
    address = 'tests/test_video/big_chungus.mp4'
    response = server.add_camera(address, 'Video', False)
    stats = server.client_stats(address)
    
    assert response is True
    assert stats['is_connected'] is True


def test_test_add_client_same_address():
    server = Server('127.0.0.1')
    address = 'tests/test_video/big_chungus.mp4'
    response1 = server.add_camera(address, 'Video', False)
    response2 = server.add_camera(address, 'Video', False)

    assert response1 is True
    assert response2 is False


def test_add_clients():
    server = Server('127.0.0.1')
    address1 = 'tests/test_video/big_chungus.mp4'
    response1 = server.add_camera(address1, 'Video', False)
    stats1 = server.client_stats(address1)

    address2 = 'tests/test_video/still_grey.mp4'
    response2 = server.add_camera(address2, 'Video', False)
    stats2 = server.client_stats(address2)

    assert response1 is True
    assert response2 is True
    assert server.cam_count == 2
    assert stats1['is_connected'] is True
    assert stats2['is_connected'] is True


def test_server_receives_frames():
    server = Server('127.0.0.1')
    address = 'tests/test_video/big_chungus.mp4'
    response = server.add_camera(address, 'Video', False)

    # let server run for 0.5 second then check client stats
    thread = Thread(target=server.run, args=(False,))
    thread.start()
    sleep(0.5)
    server.live = False
    thread.join()
    stats = server.client_stats(address)

    assert response is True
    assert stats['is_frames'] is True
    
    
def test_frames_without_movement():
    server = Server('127.0.0.1')
    address = 'tests/test_video/still_grey.mp4'
    response = server.add_camera(address, 'Video', False)
    # let server run for 0.5 second then check client stats
    thread = Thread(target=server.run, args=(False,))
    thread.start()
    sleep(0.5)
    server.live = False
    thread.join()
    stats = server.client_stats(address)
    
    assert response is True
    assert stats['is_movement'] is False


def test_frames_with_movement():
    server = Server('127.0.0.1')
    address = 'tests/test_video/big_chungus.mp4'
    response = server.add_camera(address, 'Video', False)
    # let server run for 1 second then check client stats
    thread = Thread(target=server.run, args=(False,))
    thread.start()
    sleep(1)
    server.live = False
    thread.join()
    stats = server.client_stats(address)
    
    assert response is True
    assert stats['is_movement'] is True

