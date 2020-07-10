"""Code to do label detection on an image uploaded to S3."""

import os
import urllib
import json

import boto3
from botocore.exceptions import ClientError


def get_rekognition_client():
    """Get client for the rekognition service."""
    return boto3.client('rekognition')


def get_dynamodb_resource():
    """Get client for the dynamodb service."""
    return boto3.resource('dynamodb')


def start_label_detection(bucket_name, object_name):
    """Analyse video by callig rekognition label detection service."""
    print('processing video to detect labels in : ' +
          f'{bucket_name} : {object_name}')

    try:
        response = get_rekognition_client().start_label_detection(
            Video={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': object_name
                }
            },
            NotificationChannel={
                'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
                'RoleArn': os.environ['REKOGNITION_SNS_ROLE_ARN']
            })
        print(response)
    except ClientError as client_error:
        print(str(client_error))


def start_processing_video(event, context):
    """Start the video processing pipeline.

    Main Entry point for the AWS Lambda Function
    """
    if not event.get('Records'):
        print(f'No Records to process : {event}')
        return

    for record in event['Records']:
        start_label_detection(
            record['s3']['bucket']['name'],
            urllib.parse.unquote_plus(record['s3']['object']['key']))

    return


class VideoLabelsException(Exception):
    """Exception class For the Video Labels Analysis."""

    def __init__(self, response, err_msg):
        """Initialize the Video Labels Exception class."""
        self.err_msg = err_msg
        self.response = response
        super().__init__()

    def get_response(self):
        """Get the error response."""
        return self.response

    def __str__(self):
        """Get the string rep of this class."""
        return self.err_msg


def get_video_labels(job_id):
    """Iterate over all video labels."""
    put_threshold = int(os.environ['DYNAMODB_PUT_THRESHOLD'])

    response = None
    next_page = None
    next_token = True
    params = {'JobId': job_id}
    yield_remaining = True
    while next_token:
        try:
            next_page = get_rekognition_client().\
                get_label_detection(**params)
            yield_remaining = True
        except ClientError as client_error:
            raise VideoLabelsException(response, str(client_error))

        if not response:
            response = next_page

        if next_page['JobStatus'] != 'SUCCEEDED':
            err_msg = next_page.get('StatusMessage', None)
            labels = response.get('Labels', None)

            if labels:
                next_page['Labels'] = labels
                prefix_str = 'Video analysis partially suceeded'
            else:
                prefix_str = 'Video analysis failed'

            if not err_msg:
                err_msg = prefix_str
            else:
                err_msg = f'{prefix_str} : {err_msg}'

            raise VideoLabelsException(next_page, err_msg)

        response['Labels'].extend(next_page['Labels'])

        if len(response['Labels']) >= put_threshold:
            yield response
            response['Labels'] = []
            yield_remaining = False

        next_token = next_page.get('NextToken', None)

        if next_token:
            params['NextToken'] = next_token

    if yield_remaining:
        yield response


def float_to_str(data):
    """Convert float to string."""
    if isinstance(data, dict):
        for key, val in data.items():
            data[key] = float_to_str(val)
        return data

    if isinstance(data, list):
        for index, val in enumerate(data):
            data[index] = float_to_str(val)
        return data

    if isinstance(data, float):
        return str(data)

    return data


def add_labels(videos_table, bucket_name, object_name, data):
    """Add Labels to Dynamodb table."""
    data.pop('JobStatus', None)
    data.pop('StatusMessage', None)
    data.pop('NextToken', None)
    data.pop('ResponseMetadata')

    data['VideoName'] = object_name
    data['VideoBucket'] = bucket_name

    data = float_to_str(data)

    videos_table.put_item(Item=data)


def update_labels(videos_table, object_name, data):
    """Update Labels In Dynamodb table."""
    data = data.get('Labels', None)
    if not data:
        print('No Labels data found : nothing to update')
        return

    data.pop('Timestamp', None)
    data = float_to_str(data)

    videos_table.update_item(
        Key={
            'VideoName': object_name
        },
        UpdateExpression='SET Labels = list_append(Labels, :labels)',
        ExpressionAttributeValues={
            ':labels': data
        })


def put_labels_in_db(data, bucket_name, object_name, add_update_flag):
    """Store Labels and metadata in dynamodb."""
    try:
        table_name = os.environ['DYNAMODB_TABLE_NAME']
        videos_table = get_dynamodb_resource().Table(table_name)
        if add_update_flag:
            add_labels(videos_table, bucket_name, object_name, data)
        else:
            update_labels(videos_table, object_name, data)
    except ClientError as client_error:
        raise VideoLabelsException(None, str(client_error))


def handle_label_detection(event, context):
    """Get and process results from the processing stage.

    Main Entry point for the AWS Lambda Function
    """
    if not event.get('Records'):
        print('No Events Of Interest...Aborting : {event}')
        return

    for record in event['Records']:
        sns_msg = json.loads(record['Sns']['Message'])
        bucket_name = sns_msg['Video']['S3Bucket']
        object_name = sns_msg['Video']['S3ObjectName']
        status = sns_msg['Status']
        job_id = sns_msg['JobId']

        msg_str = 'Video Analysis Succeeded'
        if status == 'SUCCEEDED':
            add_update_flag = True
            try:
                for response in \
                        get_video_labels(job_id):
                    put_labels_in_db(response, bucket_name,
                                     object_name, add_update_flag)
                    add_update_flag = False
            except VideoLabelsException as label_error:
                response = label_error.get_response()
                msg_str = str(label_error)
                if response:
                    put_labels_in_db(response, bucket_name,
                                     object_name, add_update_flag)
        else:
            msg_str = f'Video Analysis Failed : status={status}'

        print(f'{msg_str} : {bucket_name} : {object_name}')

    return
