import boto3
from abc import ABC


class ServiceGateway(ABC):
    def __init__(self, service):
        print("Initializing new service [" + service + "]")
        # self.service = boto3.resource(service)
        # self.service = boto3.client(service, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

    def data_type(self, obj):
        if type(obj) == str:
            return 'String'
        if type(obj) == int:
            return 'Number'


class SQSQueue(ServiceGateway):
    def __init__(self, url):
        super().__init__('sqs')
        # self.queue = self.service.Queue(url)

    def __convert_dictionary__(self, obj):
        return {key: {'DataType': self.data_type(
            obj[key]), 'StringValue': str(obj[key])} for key in obj}

    def send_message(self, messageattributes: dict, messagebody: str, messagegroupid: str, deduplicationid):
        return self.queue.send_message(
            MessageAttributes=self.__convert_dictionary__(messageattributes),
            MessageBody=messagebody,
            MessageGroupId=messagegroupid,
            MessageDeduplicationId=deduplicationid
        )

    def recieve_and_delete_message(self, maxnumberofmessages: int = 1, messageattributenames: list = ['All']):
        response = self.queue.receive_messages(
            AttributeNames=['SentTimestamp'],
            MaxNumberOfMessages=maxnumberofmessages,
            MessageAttributeNames=messageattributenames,
            VisibilityTimeout=0,
            WaitTimeSeconds=0
        )

        message = response[0]
        message_id = message.message_id
        receipt_handle = message.receipt_handle

        deleteresponse = self.queue.delete_messages(Entries=[{
            'Id': message_id,
            'ReceiptHandle': receipt_handle
        }])

        return message, response, deleteresponse


class S3Bucket(ServiceGateway):
    def __init__(self, bucket):
        super().__init__('s3')
        # self.bucket = self.service.Bucket(bucket)

    def upload_file(self, metadata, filename_to_upload, file_object):
        response = None
        try:
            response = self.bucket.put_object(
                Metadata=metadata, Key=filename_to_upload, Body=file_object)
        except Exception as e:
            response = e
        return response

    def get_bucket_names(self):
        return self.service.buckets.all()

    def delete_file(self, filename):
        response = self.bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': filename
                    },
                ]
            }
        )
        return response
