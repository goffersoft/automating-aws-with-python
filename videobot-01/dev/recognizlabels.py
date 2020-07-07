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
