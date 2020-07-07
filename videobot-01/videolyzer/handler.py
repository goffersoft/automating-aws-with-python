"""Code to do label detection on an image uploaded to S3."""

import urllib
import boto3


def start_label_detection(bucket_name, object_key_name):
    """Analyse video by callig rekognition label detection service."""
    print('processing video to detect labels in : ' +
          f'{bucket_name} : {object_key_name}')

    client = boto3.client('rekognition')
    response = client.start_label_detection(
        Video={'S3Object': {
                  'Bucket': bucket_name,
                  'Name': object_key_name}})

    print(response)

    return


def start_processing_video(event, context):
    """Start the video processing pipeline.

    Main Entry point for the AWS LAmbda Function
    """
    if not event.get('Records'):
        print(f'No Records to process {event}')

    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'],
            urllib.parse.unquote_plus(record['s3']['object']['key']))

    return
