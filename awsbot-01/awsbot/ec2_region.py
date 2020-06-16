#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Region Manager Class."""

from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class EC2RegionManager():
    """EC2 Region Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 Region Manager Class."""
        self.ec2_session = ec2_session

    def list_regions(self, region_names=None, pfunc=None):
        """Get regions associated with region-names."""

        def default_print(region):
            print(f'{region["RegionName"]} : {region["Endpoint"]}')

        if not pfunc:
            pfunc = default_print

        try:
            for region in self.get_regions(region_names):
                pfunc(region)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def get_regions(self, region_names):
        """Iterate over EC2 regions.

        comma separated list of region names.
        """
        if not region_names:
            region_names = []
        else:
            region_names, err = util.convert_to_list(region_names)
            if err:
                return False, err

        for region in self.ec2_session.get_ec2_client().\
                describe_regions(
                    RegionNames=region_names)['Regions']:
            yield region

        return True, None


if __name__ == '__main__':
    pass
