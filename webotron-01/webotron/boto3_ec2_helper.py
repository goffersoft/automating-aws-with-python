#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 EC2 helper function."""

import boto3_helper


def get_ec2_resource():
    """Get ec2 resource."""
    return boto3_helper.get_resource('ec2')


def get_ec2_client():
    """Get ec2 client."""
    return boto3_helper.get_client('ec2')


if __name__ == '__main__':
    pass
