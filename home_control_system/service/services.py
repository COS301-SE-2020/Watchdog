import os
import json
import datetime
import requests
from hashlib import sha256
from warrant.aws_srp import AWSSRP
from .user import User, authenticate_user


BASE_URL = "https://aprebrte8g.execute-api.af-south-1.amazonaws.com/testing"


def detect_intruder_integration():
    path = "data/temp/images"
    file_name = "test.jpeg"
    tag = "detected"
    response = upload_to_s3(path, file_name, tag)
    print(response)


def get_token():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"


def login(username, password, post_site=True):
    # authenticate user
    is_valid = authenticate_user(username, password)
    # generate user data for a user that logs into the system for the first time on a specific computer
    if is_valid:
        user = User.get_instance()
        if user is None:
            return False
        hcp_id = "s"+sha256((str(datetime.datetime.now().timestamp()) + user.user_id).encode('ascii')).hexdigest()

        user_logged_in_before = False
        user_details = {}
        if os.path.exists('.hash'):     # at least one user has logged on this computer before
            f = open('.hash', 'r')
            user_details = json.loads(f.read())
            f.close()
            if user.username in user_details:     # new user logging into the HCP on this computer
                user_logged_in_before = True
                hcp_id = user_details[user.username]['hcp_id']

        user.set_hcp_id(hcp_id)
        if not user_logged_in_before:   # persistently store the HCP id of the new user.
            user_details.update(user.__str__())
            f = open('.hash', 'w')
            f.write(json.dumps(user_details))
            f.close()
            if post_site:
                upload_site()

    return is_valid


def upload_site():
    api_endpoint = BASE_URL + '/sites'
    user = User.get_instance()
    if user is None:
        print("\033[31mCould not Upload site because you have not authenticated a valid user!")
        return 400
    response = requests.post(
        api_endpoint,
        params={
            "site_id": user.hcp_id
        },
        json={},
        headers={'Authorization': user.get_token()}
    )
    return response


def upload_camera(camera_id, metadata):
    api_endpoint = BASE_URL+"/cameras"
    user = User.get_instance()
    if user is None:
        print(f"\033[31mCould not Upload {camera_id} because you have not authenticated a valid user!")
        return 400
    token = user.get_token()
    response = requests.post(
        api_endpoint,
        params={
            "site_id": user.hcp_id,
            "camera_id": camera_id
        },
        json={
            "address": metadata['address'],
            "port": metadata['port'],
            "room": metadata['room'],
            "protocol": metadata['protocol']
        },
        headers={'Authorization': token}
    )
    return response


def upload_to_s3(path_to_resource, file_name, tag, camera_id, timestamp=None):
    user = User.get_instance()
    if user is None:
        print(f"\033[31mCould not Upload {file_name} to S3 because you have not authenticated a valid user!")
        return 400
    if timestamp is None:
        timestamp = str(datetime.datetime.now().timestamp())
    path = f"{path_to_resource}/{file_name}"
    possible_tags = ['detected', 'periodic', 'movement', 'intruder']
    if os.path.exists(path):
        if tag in possible_tags:
            # get S3 url to post image to
            # api_endpoint = BASE_URL+'/storage/upload'
            api_endpoint = 'https://aprebrte8g.execute-api.af-south-1.amazonaws.com/beta/storage/upload'
            uuid = 'demo1'  # TODO: include confidential pyPi to store global variables
            token = get_token()
            response = requests.post(
                api_endpoint, params=
                {
                    "file_name": file_name,
                    "tag": tag,
                    "user_id": user.user_id,
                    "camera_id": camera_id,
                    "timestamp": timestamp
                },
                headers={'Authorization': user.get_token()}
            )
            response = json.loads(response.text)
            # Upload video/image to bucket
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
