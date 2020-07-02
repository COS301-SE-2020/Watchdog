import requests
import json
from warrant.aws_srp import AWSSRP
import os


def get_token():
    client_id = "5bl2caob065vqodmm3sobp3k7d"
    user_pool_id = "eu-west-1_mQ0D78123"

    aws = AWSSRP(username='test', password='Test123@', pool_id=user_pool_id,
                 client_id=client_id, pool_region='eu-west-1')
    token = aws.authenticate_user()
    return token["AuthenticationResult"]["AccessToken"]


def upload_to_s3(path_to_resource, file_name, tag):
    path = f"{path_to_resource}/{file_name}"
    possible_tags = ['detected', 'periodic', 'movement', 'intruder']
    if os.path.exists(path):
        if tag in possible_tags:
            # get S3 url to post image to
            api_endpoint = 'https://aprebrte8g.execute-api.af-south-1.amazonaws.com/beta/storage/upload'
            uuid = 'demo1'  # TODO: include confidential pyPi to store global variables
            token = get_token()
            response = requests.post(
                api_endpoint, params=
                {
                    "file_name": file_name,
                    "tag": tag,
                    "user_id": uuid
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
