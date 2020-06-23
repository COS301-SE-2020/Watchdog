from .services import (
    S3Bucket,
    SQSQueue
)


class UploadService:
    def __init__(self, bucket_name, sqs_url):
        self.bucket = S3Bucket(bucket_name)
        self.sqs_queue = SQSQueue(sqs_url)

    async def upload(self, frame):
        metadata = frame.get_metadata()
        # store in bucket
        self.bucket.upload_file(metadata, frame)
        # attach name and send message on sqs to triger lambda
        response = self.sqs_queue.send_message(
            messageattributes=metadata,
            messagebody=hash(metadata),
            messagegroupid="watchdog.hcp.videorelay",
            deduplicationid=hash(metadata)
        )
        return response
