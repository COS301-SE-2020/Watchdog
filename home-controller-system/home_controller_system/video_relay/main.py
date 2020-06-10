from __MetaDataCompiler import __MetaDataCompiler


async def send_video_frames(tag, videobuffer, sqs, bucket):
    metadata = __MetaDataCompiler(tag, videobuffer.ipaddress).BufferIdSystem()
    # store in bucket
    bucket.upload_file(metadata, videobuffer.buffer)
    # attach name and send message on sqs to triger lambda
    sqs.send_message(messageattributes=metadata, messagebody=videobuffer.name)
    return
