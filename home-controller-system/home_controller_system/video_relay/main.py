from __MetaDataCompiler import __MetaDataCompiler


async def send_video_frames(tag, frame, ipaddress, sqs, bucket):
    metadata = __MetaDataCompiler(tag, ipaddress).BufferIdSystem()
    # store in bucket
    bucket.upload_file(metadata, frame)
    # attach name and send message on sqs to triger lambda
    response = sqs.send_message(
        messageattributes=metadata,
        messagebody=hash(metadata),
        messagegroupid="watchdog.hcp.videorelay",
        deduplicationid=hash(metadata)
    )
    return response
