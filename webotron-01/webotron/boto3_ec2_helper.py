#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 EC2 helper function."""

try:
    import boto3_helper
except ModuleNotFoundError:
    from . import boto3_helper


def get_ec2_resource(session):
    """Get ec2 resource."""
    return boto3_helper.get_resource(session, 'ec2')


def get_ec2_client(session):
    """Get ec2 client."""
    return boto3_helper.get_client(session, 'ec2')


if __name__ == '__main__':
    pass
