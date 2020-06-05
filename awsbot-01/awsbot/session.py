#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Main Session Manager class."""

import boto3


class SessionManager():
    """Session Manager Class."""

    def __init__(self, profile_name=None, region_name=None,
                 region_config=None, s3_session=None,
                 r53_session=None, acm_session=None,
                 cf_session=None, ec2_session=None):
        """Initialize the session manager class."""
        if profile_name:
            self.init(profile_name, region_name,
                      region_config, s3_session,
                      r53_session, acm_session,
                      cf_session, ec2_session)
        else:
            self.session = None
            self.region_config = region_config
            self.s3_session = s3_session
            self.r53_session = r53_session
            self.acm_session = acm_session
            self.cf_session = cf_session
            self.ec2_session = ec2_session

    def init(self, profile_name, region_name=None,
             region_config=None, s3_session=None,
             r53_session=None, acm_session=None,
             cf_session=None, ec2_session=None):
        """Initialize the class with a new profile_name."""
        if region_name is None:
            self.session = boto3.Session(profile_name=profile_name)
        else:
            self.session = boto3.Session(profile_name=profile_name,
                                         region_name=region_name)
        self.s3_session = s3_session
        self.region_config = region_config
        self.r53_session = r53_session
        self.acm_session = acm_session
        self.cf_session = cf_session
        self.ec2_session = ec2_session

    def get_session(self):
        """Get session."""
        return self.session

    def get_resource(self, resource_name, region_name=None):
        """Get resource by input resource name."""
        if not region_name:
            return self.session.resource(resource_name)

        return self.session.resource(resource_name, region_name=region_name)

    def get_client(self, client_name, region_name=None):
        """Get client by input client name."""
        if not region_name:
            return self.session.client(client_name)

        return self.session.client(client_name, region_name=region_name)

    def get_region_name(self):
        """Get region name associated with this session."""
        return self.session.region_name

    def is_default_region(self, region=None):
        """Validate aws region in session is 'us-east-1.

        Check and see if region associated with session is us-east-1(default)
        """
        if not region:
            return self.session.region_name == self.get_default_region()

        return region == self.s3_session.get_session().get_default_region()

    def set_s3_session(self, s3_session):
        """Set the S3 session."""
        self.s3_session = s3_session

    def get_s3_session(self):
        """Get the S3 session."""
        return self.s3_session

    def set_r53_session(self, r53_session):
        """Set the route 53 session."""
        self.r53_session = r53_session

    def get_r53_session(self):
        """Get the route 53 session."""
        return self.r53_session

    def set_acm_session(self, acm_session):
        """Set the AWS Cert. Manager session."""
        self.acm_session = acm_session

    def get_acm_session(self):
        """Get the AWS Cert. Manager session."""
        return self.acm_session

    def set_cf_session(self, cf_session):
        """Set the cloud front session."""
        self.cf_session = cf_session

    def get_cf_session(self):
        """Get the cloud front session."""
        return self.cf_session

    def set_ec2_session(self, ec2_session):
        """Set the EC2 session."""
        self.ec2_session = ec2_session

    def get_ec2_session(self):
        """Get the EC2 session."""
        return self.ec2_session

    def get_region_config(self):
        """Get AWS region map."""
        return self.region_config

    def set_region_config(self, region_config):
        """Set the AWS region map."""
        self.region_config = region_config

    @staticmethod
    def get_default_region():
        """Get default region."""
        return 'us-east-1'

    @staticmethod
    def get_client_error_code(err_response):
        """Get client error code from the response."""
        return err_response.response['Error']['Code']

    @staticmethod
    def get_client_http_status_code(client_response):
        """Get client http status code."""
        return client_response['ResponseMetadata']['HTTPStatusCode']

    @staticmethod
    def is_ok_response(client_response):
        """Get client http response code.

        Return True, hcode if response code is
        between 200 and 299
        Return Falsei otherwise
        """
        hcode = SessionManager.get_client_http_status_code(client_response)
        if hcode in range(200, 300):
            return True, hcode

        return False, hcode

    @staticmethod
    def is_error_response(client_response):
        """Get client http response code.

        Return False, rcode if response code is
        between 200 and 299
        Return True, rcode otherwise
        """
        status, hcode = SessionManager.is_ok_response(client_response)

        return not status, hcode


if __name__ == '__main__':
    pass
