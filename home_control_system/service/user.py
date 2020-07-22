import os
import sys
import json
import traceback
from warrant import AWSSRP, Cognito
from datetime import datetime, timedelta
from .config import configure


configure()
conf = json.loads(os.environ['config'])
client_id = conf['services']['client']['id']
user_pool_id = conf['services']['client']['pool']


class User:
    __instance = None

    # Singleton User of HCP
    @staticmethod
    def get_instance(metadata=None):
        if User.__instance is None:
            try:
                User(metadata)
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_tb)
                return None
        return User.__instance

    def __init__(self, metadata):
        if User.__instance is None:
            User.__instance = self
        if metadata is None:
            raise Exception("Metadata map not provided for user...")

        self.hcp_id = None
        self.user_id = metadata['user_id']
        self.username = metadata['username']
        self.password = metadata['password']
        self.token = {
            'token': '',
            'expiration': ''
        }
        self.generate_token()

    def generate_token(self):
        aws = AWSSRP(
            username=self.username,
            password=self.password,
            pool_id=user_pool_id,
            client_id=client_id,
            pool_region='eu-west-1'
        )
        token = aws.authenticate_user()
        expires_in = int(token["AuthenticationResult"]['ExpiresIn'])
        expires_in = datetime.now() + timedelta(seconds=expires_in)
        self.token['token'] = token["AuthenticationResult"]["IdToken"]
        self.token['expiration'] = str(expires_in.timestamp())

    def get_token(self):
        now = str(datetime.now().timestamp())
        if now > self.token['expiration']:
            self.generate_token()
        return self.token['token']

    def set_hcp_id(self, hcp_id):
        self.hcp_id = hcp_id

    def __str__(self):
        return {
            self.username: {
                "hcp_id": self.hcp_id
            }
        }


def authenticate_user(username, password):
    try:
        u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
        u.authenticate(password=password)
        user = u.get_user(attr_map={"user_id": "sub"})
        user_id = user.sub
    except Exception as e:
        print("Incorrect username or password, please try again" + str(e))
        return False

    user_data = {
        'user_id': user_id,
        "username": username,
        "password": password
    }

    User.get_instance(user_data)  # instantiate singleton object
    return True




