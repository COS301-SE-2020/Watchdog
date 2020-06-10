import boto3
from botocore.exceptions import ClientError
from abc import ABC
from decorators import singleton


class APIConnectionProxy(ABC):
    def __init__(self, service):
        self.service = boto3.client(service)

    def data_type(self, obj):
        if type(obj) == 'str':
            return 'String'
        if type(obj) == 'int':
            return 'Number'


class SQSQueue(APIConnectionProxy):
    def __init__(self, url):
        super('sqs')
        self.url = url

    def __convert_dictionary__(self, obj):
        return {key: {'DataType': self.data_type(
            obj[key]), 'StringValue': obj[key]} for key in obj}

    def send_message(self, messageattributes: dict, messagebody: str):
        return self.service.send_message(
            QueueUrl=self.url,
            MessageAttributes=self.__convert_dictionary__(messageattributes),
            MessageBody=messagebody
        )

    def recieve_and_delete_message(self, maxnumberofmessages: int = 1, messageattributenames: list = ['All']):
        response = self.service.recieve_message(
            QueueUrl=self.url,
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=maxnumberofmessages,
            MessageAttributeNames=messageattributenames,
            VisabilityTimeout=0,
            WaitTimeSeconds=0
        )

        message = response['Messages'][0]
        receipt_handle = message['RecieptHandle']

        self.service.delete_message(
            QueueUrl=self.url, RecieptHandle=receipt_handle)

        return response


class S3Bucket(APIConnectionProxy):
    def __init__(self, bucket):
        super('s3')
        self.bucket = bucket

    def upload_file(self, metadata, filename_to_upload, object_name=None):
        if object_name is None:
            object_name = filename_to_upload
        response = None
        try:
            response = self.service.upload_file(
                filename_to_upload,
                self.bucket,
                object_name,
                ExtraArgs={'Metadata': metadata}
            )
        except ClientError as e:
            response = e

        return response
