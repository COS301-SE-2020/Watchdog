import requests
import json
import os
import datetime
from hashlib import sha256
from service.user import User, authenticate_user

BASE_URL = "https://aprebrte8g.execute-api.af-south-1.amazonaws.com/testing"


def login(username, password, post_site=True):
    # authenticate user
    is_valid = authenticate_user(username, password)
    # generate user data for a user that logs into the system for the first time on a specific computer
    if is_valid:
        user = User.get_instance()
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


def upload_to_s3(path_to_resource, file_name, tag):
    user = User.get_instance()
    token = user.token
    path = f"{path_to_resource}/{file_name}"
    possible_tags = ['detected', 'periodic', 'movement', 'intruder']
    if os.path.exists(path):
        if tag in possible_tags:
            # get S3 url to post image to
            api_endpoint = BASE_URL+'/storage/upload'
            response = requests.post(
                api_endpoint, params=
                {
                    "file_name": file_name,
                    "tag": tag,
                    "user_id": user.user_id,
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
