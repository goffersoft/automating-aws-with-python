from boto3_helper import *


def get_ec2_resource():
    """ get ec2 resource """

    return get_resource('ec2')


def get_ec2_client():
    """ get ec2 client """

    return get_client('ec2')


if __name__ == '__main__':
    pass
