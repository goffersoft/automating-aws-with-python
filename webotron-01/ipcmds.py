# coding: utf-8
import boto3
session = boto3.Session(profile_name='python_automation')
ec2_resource = session.resource('ec2')
s3_resource = session.resource('s3')
ec2_client = session.client('ec2')
s3_client = session.client('s3')
