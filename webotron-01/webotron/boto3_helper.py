#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Boto3 helper functions."""


def get_default_region():
    """Get default region."""
    return 'us-east-1'


def get_client_error_code(err_response):
    """Get client error code from the response."""
    return err_response.response['Error']['Code']


if __name__ == '__main__':
    pass
