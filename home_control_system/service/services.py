import requests
import json
from warrant import AWSSRP, Cognito
import os
import datetime
from hashlib import sha256


def login(username, password):
    # authenticate user
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"
    try:
        u = Cognito(client_id=client_id, user_pool_id=user_pool_id, username=username, user_pool_region='eu-west-1')
        u.authenticate(password=password)
        user = u.get_user(attr_map={"user_id": "sub"})
        user_id = user.sub
    except Exception as e:
        print("incorrect username or password")
        return
    # generate user data for a user that logs into the system for the first time on a specific computer
    hcp_id = sha256((str(datetime.datetime.now().timestamp()) + user_id).encode('ascii')).hexdigest()
    user_logged_in_before = False
    user = {
        user_id: {
            'user_id': user_id,
            "username": username,
            "hcp_id": hcp_id
        },
    }
    if os.path.exists('.hash'):     # at least one user has logged on this computer before
        # TODO: encrypt hash file to prevent it being accessible to user as raw text
        # user_details = sha256(str(user_details).encode()).hexdigest()
        f = open('.hash', 'r')
        user_details = json.loads(f.read())
        f.close()
        if user_id not in user_details:     # new user logging into the HCP on this computer
            user_details.update(user)
        else:
            user = user_details    # previous user has logged into the HCP on this computer
            user_logged_in_before = True
    else:
        user_details = user     # first user to log into the HCP in this computer

    u = open('.current_user', 'w')  # write the details of the current user logged in on this computer
    u.write(json.dumps(user[user_id]))
    u.close()

    if not user_logged_in_before:   # persistently store the new user that logged into the HCP on this computer
        f = open('.hash', 'w')
        f.write(json.dumps(user_details))
        f.close()


def get_current_user_details() -> dict:
    if os.path.exists('.current_user'):
        f = open('.current_user', 'r')
        user_details = f.read()
        user_details = json.loads(user_details)
        return user_details


def get_token():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"
    aws = AWSSRP(username='test', password='Test123@', pool_id=user_pool_id,
                 client_id=client_id, pool_region='eu-west-1')
    token = aws.authenticate_user()
    return token["AuthenticationResult"]["AccessToken"]


def upload_to_s3(path_to_resource, file_name, tag):
    user_details = get_current_user_details()
    token = get_token()
    path = f"{path_to_resource}/{file_name}"
    possible_tags = ['detected', 'periodic', 'movement', 'intruder']
    if os.path.exists(path):
        if tag in possible_tags:
            # get S3 url to post image to
            api_endpoint = 'https://aprebrte8g.execute-api.af-south-1.amazonaws.com/beta/storage/upload'
            response = requests.post(
                api_endpoint, params=
                {
                    "file_name": file_name,
                    "tag": tag,
                    "user_id": user_details['user_id'],
                    "camera_id": "2321"
                },
                headers={'Authorization': f'TOK:{token}'}
            )
            response = json.loads(response.text)
            # upload image to bucket
            with open(path, 'rb') as binary_object:
                files = {
                    'file': (file_name, binary_object)
                }
                response = requests.post(response['url'], data=response['fields'], files=files)
                print("POST response" + str(response))
            return 200
        else:
            print("The tag that you provided is invalid!"
                  "\nIf you want to upload videos: tag must be either movement, periodic, or intruder"
                  "\nIf you want to upload a detected image: tag must be detected")
    else:
        print("File not found! Please ensure that the file path is correct!, current path provided: " + path +
              "\nNOTE: the first parameter is the path to the resource without a leading backslash")
    return 500
