#! /usr/bin/python
# coding: utf-8

import boto3


if __name__ == '__main__':
    session = boto3.Session(profile_name='python_automation')
    ec2c = session.client('ec2')
    asc = session.client('autoscaling')
    asc.describe_auto_scaling_groups()
    asc.describe_policies()
    asc.execute_policy(AutoScalingGroupName='Notifon Example', PolicyName='Scale Up')
