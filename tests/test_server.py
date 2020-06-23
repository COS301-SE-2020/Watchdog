from time import sleep
from threading import Thread
from home_control_system.server.server import Server

# UNIT-TESTS
#   1 -- test_add_client
#   2 -- test_test_add_client_same_address
#   3 -- test_add_clients
#   4 -- test_serve_receives_frames
#   5 -- test_frames_without_movement
#   6 -- test_frames_with_movement

def test_add_client():
    serve = Server('127.0.0.1')
    address = 'data/sample/big_chungus.mp4'
    response = serve.add_camera(address, '', '', 'Video', '')
    stats = serve.client_stats(address)

    assert response is True
    assert stats['is_connected'] is True


def test_test_add_client_same_address():
    serve = Server('127.0.0.1')
    address = 'data/sample/big_chungus.mp4'
    response1 = serve.add_camera(address, '', '', 'Video', '')
    response2 = serve.add_camera(address, '', '', 'Video', '')

    assert response1 is True
    assert response2 is False


def test_add_clients():
    serve = Server('127.0.0.1')

    address1 = 'data/sample/big_chungus.mp4'
    response1 = serve.add_camera(address1, '', '', 'Video', '')
    stats1 = serve.client_stats(address1)

    address2 = 'data/sample/still_grey.mp4'
    response2 = serve.add_camera(address2, '', '', 'Video', '')
    stats2 = serve.client_stats(address2)

    assert response1 is True
    assert response2 is True
    assert len(serve.cameras) == 2
    assert stats1['is_connected'] is True
    assert stats2['is_connected'] is True


def test_serve_receives_frames():
    serve = Server('127.0.0.1')
    address = 'data/sample/big_chungus.mp4'
    response = serve.add_camera(address, '', '', 'Video', '')

    # let serve run for 0.5 second then check client stats
    thread = Thread(target=serve.run, args=(False,))
    thread.start()
    sleep(0.5)
    serve.live = False
    thread.join()

    stats = serve.client_stats(address)

    assert response is True
    assert stats['is_frames'] is True


def test_frames_without_movement():
    serve = Server('127.0.0.1')
    address = 'data/sample/still_grey.mp4'
    response = serve.add_camera(address, '', '', 'Video', '')

    # let serve run for 0.5 second then check client stats
    thread = Thread(target=serve.run, args=(False,))
    thread.start()
    sleep(0.5)
    serve.live = False
    thread.join()

    stats = serve.client_stats(address)

    assert response is True
    assert stats['is_movement'] is False


def test_frames_with_movement():
    serve = Server('127.0.0.1')
    address = 'data/sample/big_chungus.mp4'
    response = serve.add_camera(address, '', '', 'Video', '')

    # let serve run for 1 second then check client stats
    thread = Thread(target=serve.run, args=(False,))
    thread.start()
    sleep(1)
    serve.live = False
    thread.join()

    stats = serve.client_stats(address)

    assert response is True
    assert stats['is_movement'] is True
