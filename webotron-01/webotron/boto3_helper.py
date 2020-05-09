import boto3
from botocore.exceptions import ClientError

g_boto3_session = None


def get_session():
    """ get boto3 session """

    return g_boto3_session


def get_resource(rname):
    """ get resource by input resource name """

    return get_session().resource(rname)


def get_client(cname):
    """ get client by input client name """

    return get_session().client(cname)


def is_default_region():
    """ check to see if region associated with session is us-east-1(default)"""

    return get_session().region_name == 'us-east-1'


def getClientErrorCode(e):
    """ get client error code from the response """

    return e.response['Error']['Code']


def init(pname='python_automation', rname=None):
    """ initialize webotron script """

    global g_boto3_session

    if rname is None:
        g_boto3_session = boto3.Session(profile_name=pname)
    else:
        g_boto3_session = boto3.Session(profile_name=pname, region_name=rname)


if __name__ == '__main__':
    pass
