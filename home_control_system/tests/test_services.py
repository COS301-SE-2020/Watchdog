
VIDEO_RELAY_QUEUE = "https://sqs.af-south-1.amazonaws.com/878292117449/VideoReceiver.fifo"
USER_CONTENT_BUCKET = "watchdog.uservideocontent"

# This needs to be changed to use the Service classes

# def test_connect_bucket():
#     s3 = create_service('S3Bucket', USER_CONTENT_BUCKET)
#     buckets = s3.get_bucket_names()
#     names = [bucket.name for bucket in buckets]
#     assert USER_CONTENT_BUCKET in names


# def test_upload_file():
#     s3 = create_service('S3Bucket', USER_CONTENT_BUCKET)
#     response = None
#     with open('tests/test.txt', 'rb') as data:
#         response = s3.upload_file({}, "test.txt", data)
#     assert response.key == 'test.txt' and response.bucket_name == USER_CONTENT_BUCKET


# def test_delete_file():
#     s3 = create_service('S3Bucket', USER_CONTENT_BUCKET)
#     response = s3.delete_file('test.txt')
#     assert len(response['Deleted']) != 0


# def test_connect_queue():
#     queue = create_service('SQSQueue', VIDEO_RELAY_QUEUE)
#     assert queue is not None


# def test_send_message():
#     queue = create_service('SQSQueue', VIDEO_RELAY_QUEUE)
#     response = queue.send_message(
#         {"testing": 1}, "this is a test message", "hcp.testing", "unit_test")
#     assert response is not None


# def test_recieve_and_delete_message():
#     queue = create_service('SQSQueue', VIDEO_RELAY_QUEUE)
#     message = queue.recieve_and_delete_message()
#     assert message is not None


# test_connect_queue()
# test_send_message()
# test_recieve_and_delete_message()
# test_connect_bucket()
# test_upload_file()
# test_delete_file()
