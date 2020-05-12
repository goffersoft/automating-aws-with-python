#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 helper functions."""

import boto3

g_boto3_session = None


def get_session():
    """Get boto3 session."""
    return g_boto3_session


def get_resource(rname):
    """Get resource by input resource name."""
    return get_session().resource(rname)


def get_client(cname):
    """Get client by input client name."""
    return get_session().client(cname)


def get_default_region():
    """Get default region."""
    return 'us-east-1'


def is_default_region():
    """Validate aws region in session is 'us-east-1.

    Check and see if region associated with session is us-east-1(default)
    """
    return get_session().region_name == get_default_region()


def get_client_error_code(err_response):
    """Get client error code from the response."""
    return err_response.response['Error']['Code']


def init(pname='python_automation', rname=None):
    """Initialize webotron script."""
    global g_boto3_session

    if rname is None:
        g_boto3_session = boto3.Session(profile_name=pname)
    else:
        g_boto3_session = boto3.Session(profile_name=pname, region_name=rname)


if __name__ == '__main__':
    pass
