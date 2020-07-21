from service.user import authenticate_user, User


def test_get_user():
    username = 'Foo'
    password = 'Test@123'
    is_valid = authenticate_user(username=username, password=password)
    user = User.get_instance()

    assert is_valid == True
    assert user.username == username
    assert user.password == password

