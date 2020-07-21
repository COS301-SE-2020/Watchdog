from service.services import *
from warrant import Cognito
from hashlib import sha256
from service.user import User


def test_valid_login():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"
    username = 'Foo'
    password = 'Test@123'

    login(username, password, False)
    user_details = User.get_instance()

    u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
    u.authenticate(password=password)
    user = u.get_user(attr_map={"user_id": "sub"})

    assert user_details.user_id == user.sub
    assert user_details.username == user.username
    assert user_details.hcp_id != 0


def test_upload_camera():
    is_valid = authenticate_user(username="Foo", password="Test@123")
    user = User.get_instance()
    # this is a valid site_id - in case the .hash file was deleted
    user.set_hcp_id("sd185c3eebe4248c0be902500f37b98858df09791847cd8ecf33d3a34ae3ef5ae")

    metadata = {
        "address": '127.0.0.1',
        "port": '5000',
        "room": 'backyard',
        "protocol": 'http',
        'path':''
    }

    camera_id = "c" + sha256((str(datetime.datetime.now().timestamp())).encode('ascii')).hexdigest()
    response = upload_camera(camera_id, metadata)

    assert response.status_code == 200
    assert is_valid == True


def test_upload_video():
    # upload a sample video with the tag periodic
    # hard coded valid camera id in the DB - this process is automated in the HCP
    camera_id = "c544bae2687c592981070dd0bddd6ab68c49727b4a03041e59880d4f7b8fff455"
    username = 'Foo'
    password = 'Test@123'

    is_valid = authenticate_user(username=username, password=password)
    user = User.get_instance()
    # this is a valid site_id - in case the .hash file was deleted
    user.set_hcp_id("sd185c3eebe4248c0be902500f37b98858df09791847cd8ecf33d3a34ae3ef5ae")

    response = upload_to_s3(path_to_resource='data/sample', file_name='surveillance2.mp4', tag='periodic', camera_id=camera_id)

    assert is_valid == True
    assert response == 200


def test_upload_image():
    # upload a sample video with the tag periodic
    # hard coded valid camera id in the DB - this process is automated in the HCP
    camera_id = "c544bae2687c592981070dd0bddd6ab68c49727b4a03041e59880d4f7b8fff455"
    username = 'Foo'
    password = 'Test@123'

    is_valid = authenticate_user(username=username, password=password)
    user = User.get_instance()
    # this is a valid site_id - in case the .hash file was deleted
    user.set_hcp_id("sd185c3eebe4248c0be902500f37b98858df09791847cd8ecf33d3a34ae3ef5ae")

    response = upload_to_s3(path_to_resource='data/temp/images', file_name='ali.jpg', tag='detected', camera_id=camera_id)

    assert is_valid == True
    assert response == 200


def test_get_camera_config():
    username = 'Foo'
    password = 'Test@123'
    is_valid = authenticate_user(username=username, password=password)

    user = User.get_instance()
    user.set_hcp_id('sd185c3eebe4248c0be902500f37b98858df09791847cd8ecf33d3a34ae3ef5ae')
    response = get_camera_setup()

    assert len(response) > 0
    assert is_valid == True


def test_get_locations():
    username = 'Foo'
    password = 'Test@123'
    is_valid = authenticate_user(username=username, password=password)

    user = User.get_instance()
    user.set_hcp_id('sd185c3eebe4248c0be902500f37b98858df09791847cd8ecf33d3a34ae3ef5ae')
    response = get_location_setup()

    assert 'backyard' in response
    assert is_valid == True
