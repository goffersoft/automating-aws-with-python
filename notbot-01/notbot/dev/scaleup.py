#! /usr/bin/python
# coding: utf-8

import boto3

if __name__ == '__main__':
    session = boto3.Session(profile_name='python_automation')
    asc = session.client('autoscaling')
    asc.execute_policy(AutoScalingGroupName='Notifon Example', PolicyName='Scale Up')
