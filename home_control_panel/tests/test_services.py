from warrant import Cognito
from service.services import *
from service.user import User

"""
Test functions for integration with the API
"""

# Debug user valid hard coded values for testing
username = 'debug'
password = 'Test@123'
camera_id = "cad489214e688d3d4643b5a1b474f0b39455904737e7749a16cebe7d0b82063c5"


def initialize_user():
    hcp_id = 'v97d00136e2f532355e85291689d7e16138cb95cbe769ff5b8b2fab5c83132a09'
    is_valid = authenticate_user(username=username, password=password)
    user = User.get_instance()
    user.set_hcp_id(hcp_id)

    return is_valid


def test_valid_login():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"

    login(username, password)
    user_details = User.get_instance()

    u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
    u.authenticate(password=password)
    user = u.get_user(attr_map={"user_id": "sub"})

    assert user_details.user_id == user.sub
    assert user_details.username == user.username
    assert user_details.hcp_id != 0


def test_upload_camera():
    is_valid = initialize_user()

    metadata = {
        "address": '127.0.0.1',
        "port": '5000',
        "location": 'My Backyard',
        "protocol": 'http',
        'path': ''
    }

    cam_id = "c" + sha256((str(datetime.datetime.now().timestamp())).encode('ascii')).hexdigest()
    response = upload_camera(cam_id, metadata)

    assert response.status_code == 200
    assert is_valid == True


# upload a sample video with the tag periodic
def test_upload_video():
    is_valid = initialize_user()

    response = upload_to_s3(path_to_resource='data/sample', file_name='still_grey.mp4', tag='periodic', camera_id=camera_id)

    assert is_valid == True
    assert response == 200


# upload a detected image
def test_upload_image():
    is_valid = initialize_user()

    response = upload_to_s3(path_to_resource='data', file_name='IMG_5047.JPG', tag='detected', camera_id=camera_id)

    assert is_valid == True
    assert response == 200


def test_get_camera_config():
    is_valid = initialize_user()
    response = get_camera_setup()

    assert len(response) > 0
    assert is_valid == True


def test_update_location_already_exists():
    is_valid = initialize_user()

    response = update_location(old_location="backyard", new_location="backyard")

    assert is_valid == True
    assert response.status_code == 202


def test_remove_camera():
    is_valid = initialize_user()
    location = 'Testing Bedroom'
    # upload dummy camera to be deleted
    metadata = {
        "address": '0.0.0.0',
        "port": '25',
        "location": location,
        "protocol": 'http',
        'path': ''
    }

    cam_id = "c" + sha256((str(datetime.datetime.now().timestamp())).encode('ascii')).hexdigest()
    upload_camera_response = upload_camera(camera_id=cam_id, metadata=metadata)
    print("camera id:" +cam_id)
    print("dummy camera upload response:\n"+str(upload_camera_response.text))
    response = remove_camera(location=location, camera_id=cam_id)
    print("-----------------\ndelete dummy camera upload response:\n"+str(response.text))
    # check that the dummy camera was successfully inserted
    assert upload_camera_response.status_code == 200
    # check that the
    assert response.status_code == 200
