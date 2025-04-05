#!/usr/bin/env python3
import boto3
import ffmpeg
import uuid

s3 = boto3.client("s3")

def lambda_handler(event, context):
    bucket_name = event["bucket"]
    object_key = event["key"]
    thumbnail_key = object_key.rsplit(".", 1)[0] + "_thumbnail.jpg"

    TMP_VIDEO_PATH = f"/tmp/{str(uuid.uuid4())}_video.mp4"
    TMP_THUMB_PATH = f"/tmp/{str(uuid.uuid4())}_thumbnail.jpg"

    try:
        s3.download_file(bucket_name, object_key, TMP_VIDEO_PATH)

        ffmpeg.input(TMP_VIDEO_PATH, ss=1).output(TMP_THUMB_PATH, vframes=1, vf="scale=320:-1").run()

        s3.upload_file(TMP_THUMB_PATH, bucket_name, thumbnail_key, ExtraArgs={"ContentType": "image/jpeg"})

        return {"thumbnail_key": thumbnail_key}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)} 
