from service.services import *
from warrant import Cognito
from hashlib import sha256
from service.user import User


def test_valid_login():
    # NOTE: if .hash file does not exist in the root directory, it will upload a new site to the DB! Be cautious!
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"
    username = 'Foo'
    password = 'Test@123'

    login(username, password)
    user_details = User.get_instance()

    u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
    u.authenticate(password=password)
    user = u.get_user(attr_map={"user_id": "sub"})

    assert user_details.user_id == user.sub
    assert user_details.username == user.username
    assert user_details.hcp_id != 0


def test_upload_camera():
    is_valid = login(username="Foo", password="Test@123", post_site=False)
    user = User.get_instance()
    f = open('.hash', 'r')
    user_details = json.loads(f.read())
    f.close()

    user.set_hcp_id(user_details[user.username]['hcp_id'])

    metadata = {
        "address": '127.0.0.1',
        "port": '5000',
        "room": 'backyard',
        "protocol": 'http'
    }

    camera_id = "c" + sha256((str(datetime.datetime.now().timestamp())).encode('ascii')).hexdigest()
    response = upload_camera(camera_id, metadata)

    assert response.status_code == 200
    assert is_valid == True
