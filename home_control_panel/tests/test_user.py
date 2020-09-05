from service.user import authenticate_user, User

username = 'debug'
password = 'Test@123'


def test_get_user():
    is_valid = authenticate_user(username=username, password=password)
    user = User.get_instance()

    assert is_valid == True
    assert user.username == username
    assert user.password == password

