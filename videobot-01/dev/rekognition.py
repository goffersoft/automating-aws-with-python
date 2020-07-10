# coding: utf-8
import boto3
session = boto3.Session(profile_name='python_automation')
mlrecogc = session.client('rekognition')
mlrecogc.start_label_detection(Video={'S3Object': { 'Bucket': 'peasvideoanalyzer', 'Name': 'video1.mp4'}})
jobid = 'fa56766b048bc969b4d8b6b4c804cb769ffa038ecba3d43ef7986279bb69e24b'
response = mlrecogc.get_label_detection(JobId=jobid)
response
response['status']
response['StatusMessage']
response['JobStatus']
response['ResponseMetaData']
response['ResponseMetadata']
response['VideoMetadata']
response['Labels']
for entry in response['Labels']:
    print(entry['Label'])
    
for entry in response['Labels']:
    print(entry['Label']['Name'])

data['Records'][0]['s3']['bucket']['name']
data['Records'][0]['s3']['object']['key']

rekogc = session.client('rekognition')
        
for record in event['Records']:
        sns_topic_arn = record['Sns']['TopicArn']
        msg = json.loads(record['Sns']['Message'])
        job_id = msg['JobId']
        status = msg['Status']
        api_name = msg['API']
        timestamp = msg['Timestamp']
        s3_bucket_name = msg['Video']['S3Bucket']
        s3_object_name = msg['Video']['S3ObjectName']
        response = rekogc.\
            get_label_detection(JobId=job_id)
        print(sns_topic_arn)
        print(job_id)
        print(status)
        print(api_name)
        print(timestamp)
        print(s3_bucket_name)
        print(s3_object_name)
        #print(response)
