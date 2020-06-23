from .services import SQSQueue


# Detection Service
#   Has Direct Access to SQS Queue
#   Enqueues Intruder Alerts with Images
class DetectionService:
    def __init__(self, sqs_url):
        self.sqs_queue = SQSQueue(sqs_url)

    async def alert(self, body):
        print("Notifying!")
