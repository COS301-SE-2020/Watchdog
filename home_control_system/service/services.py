import os
import json
import datetime
import requests
from hashlib import sha256
from service import config
from .user import User, authenticate_user


conf = config.configure()
CONNECT = conf['services']['live']
URL = conf['services']['base_url']
BASE_URL = URL + '/testing'


# TODO: [NEEDED]
#   upload_location() - this is for the locations within the hcp i.e. Kitchen, bedroom... metadata: {id, location}


def get_location_setup():
    if not CONNECT:
        return None  # hcp has no cameras or site is not in the db
    user = User.get_instance()
    api_endpoint = BASE_URL + '/sites'
    if user.hcp_id is not None:
        response = requests.get(
            url=api_endpoint,
            params={
                "site_id": user.hcp_id
            },
            headers={'Authorization': user.get_token()}
        )
        response = json.loads(response.text)
        if len(response['data']) > 0:  # if the current control panel has cameras
            locations = []
            cameras = response['data']['control_panel'].get(user.hcp_id)['cameras']
            for camera in cameras:
                locations.append(cameras.get(camera)['room'])
            locations = list(set(locations))  # get list of no duplicate rooms
            locations = [empty_room for empty_room in locations if empty_room != ""]  # remove cameras that are not part of a room
            locations.sort()  # sort the list in alphabetical order in ascending order
            return locations


def get_camera_setup():
    if not CONNECT:
        return None  # hcp has no cameras or site is not in the db
    user = User.get_instance()
    api_endpoint = BASE_URL + '/sites'
    if user.hcp_id is not None:
        response = requests.get(
            url=api_endpoint,
            params={
                "site_id": user.hcp_id
            },
            headers={'Authorization': user.get_token()}
        )
        response = json.loads(response.text)
        if len(response['data']) > 0:  # HCP id is assigned for this user
            response = response['data']['control_panel']
            response = response.get(user.hcp_id)['cameras']
            return response


def login(username, password, post_site=True):
    if not CONNECT:
        return True
    # authenticate user
    is_valid = authenticate_user(username, password)
    # generate user data for a user that logs into the system for the first time on a specific computer
    if is_valid:
        user = User.get_instance()
        if user is None:
            return False
        hcp_id = "s" + sha256((str(datetime.datetime.now().timestamp()) + user.user_id).encode('ascii')).hexdigest()

        user_logged_in_before = False
        user_details = {}
        hash_file = 'data/.hash'
        if os.path.exists(hash_file):  # at least one user has logged on this computer before
            f = open(hash_file, 'r')
            user_details = json.loads(f.read())
            f.close()
            if user.username in user_details:  # new user logging into the HCP on this computer
                user_logged_in_before = True
                hcp_id = user_details[user.username]['hcp_id']

        user.set_hcp_id(hcp_id)
        if not user_logged_in_before:  # persistently store the HCP id of the new user.
            user_details.update(user.__str__())
            f = open(hash_file, 'w')
            f.write(json.dumps(user_details))
            f.close()
            if post_site:
                upload_site()

    return is_valid


def upload_site():
    if not CONNECT:
        return None
    api_endpoint = BASE_URL + '/sites'
    user = User.get_instance()
    if user is None:
        print("\033[31mCould not Upload site because you have not authenticated a valid user!")
        return 400
    response = requests.post(
        url=api_endpoint,
        params={
            "site_id": user.hcp_id
        },
        json={},
        headers={'Authorization': user.get_token()}
    )
    return response


def upload_camera(camera_id, metadata):
    if not CONNECT:
        return None
    api_endpoint = BASE_URL + "/cameras"
    user = User.get_instance()
    if user is None:
        print(f"\033[31mCould not Upload {camera_id} because you have not authenticated a valid user!")
        return 400
    token = user.get_token()
    response = requests.post(
        url=api_endpoint,
        params={
            "site_id": user.hcp_id,
            "camera_id": camera_id
        },
        json={
            "address": metadata['address'],
            "port": metadata['port'],
            "room": metadata['room'],
            "protocol": metadata['protocol'],
            "path": metadata['path']
        },
        headers={'Authorization': token}
    )
    print(str(response.text))
    return response


def upload_to_s3(path_to_resource, file_name, tag, camera_id, timestamp=None):
    if not CONNECT:
        return None
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
            api_endpoint = URL + '/beta/storage/upload'
            # TODO: include confidential pyPi to store global variables
            response = requests.post(
                url=api_endpoint,
                params={
                    "file_name": file_name,
                    "tag": tag,
                    "user_id": user.user_id,
                    "camera_id": camera_id,
                    "timestamp": timestamp
                },
                headers={'Authorization': user.get_token()}
            )
            if 'url' in response:
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
        print("File not found! Please ensure that the file path is correct!, current path provided: \
              " + path + "\nNOTE: the first parameter is the path to the resource without a leading backslash")
    return 500
