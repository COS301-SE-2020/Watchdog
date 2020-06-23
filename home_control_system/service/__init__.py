from service.upload import UploadService
from service.detection import DetectionService
from service.services import (
    S3Bucket,
    SQSQueue
)

__version__ = "0.1.0"

upload_api = UploadService('', '')

detection_api = DetectionService('')