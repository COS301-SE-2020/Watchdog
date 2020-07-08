from service.services import login, get_current_user_details
from warrant import Cognito


def test_valid_login():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"
    username = 'sundy'
    password = 'Test123@'

    login(username, password)
    user_details = get_current_user_details()

    u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
    u.authenticate(password=password)
    user = u.get_user(attr_map={"user_id": "sub"})

    assert user_details['user_id'] == user.sub
    assert user_details['username'] == user.username
    assert user_details['hcp_id'] != 0
