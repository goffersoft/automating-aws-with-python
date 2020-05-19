#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 EC2 helper function."""


def get_ec2_resource(session):
    """Get ec2 resource."""
    return session.get_resource('ec2')


def get_ec2_client(session):
    """Get ec2 client."""
    return session.get_client('ec2')


if __name__ == '__main__':
    pass
