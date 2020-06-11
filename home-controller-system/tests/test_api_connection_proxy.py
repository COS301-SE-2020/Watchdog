from home_controller_system import api_connection_proxy as acp
from home_controller_system import urls


def test_connect_bucket():
    s3 = acp.S3Bucket(urls.USER_CONTENT_BUCKET)
    buckets = s3.get_bucket_names()
    names = [bucket.name for bucket in buckets]
    assert urls.USER_CONTENT_BUCKET in names


def test_upload_file():
    s3 = acp.S3Bucket(urls.USER_CONTENT_BUCKET)
    response = None
    with open('tests/test.txt', 'rb') as data:
        response = s3.upload_file({}, "test.txt", data)
    assert response.key == 'test.txt' and response.bucket_name == urls.USER_CONTENT_BUCKET


def test_delete_file():
    s3 = acp.S3Bucket(urls.USER_CONTENT_BUCKET)
    response = s3.delete_file('test.txt')
    assert len(response['Deleted']) != 0


def test_connect_queue():
    queue = acp.SQSQueue(urls.VIDEO_RELAY_QUEUE)
    assert queue is not None


def test_send_message():
    queue = acp.SQSQueue(urls.VIDEO_RELAY_QUEUE)
    response = queue.send_message(
        {"testing": 1}, "this is a test message", "hcp.testing", "unit_test")
    assert response is not None


def test_recieve_and_delete_message():
    queue = acp.SQSQueue(urls.VIDEO_RELAY_QUEUE)
    message = queue.recieve_and_delete_message()
    assert message is not None


# test_connect_queue()
# test_send_message()
# test_recieve_and_delete_message()
# test_connect_bucket()
# test_upload_file()
# test_delete_file()
