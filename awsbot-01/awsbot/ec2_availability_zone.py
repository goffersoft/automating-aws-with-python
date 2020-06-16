#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Availability Zone Manager Class."""

from collections import defaultdict
from botocore.exceptions import ClientError


class EC2AvailabilityZoneManager():
    """EC2 Availability Zone Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 Availability Zone Manager Class."""
        self.ec2_session = ec2_session

    def list_availability_zones(self, pfunc=None):
        """List availability zones.

        List Availability zones associated with the
        current region only.
        """

        def default_collect(zone):
            zone_dict[zone['RegionName']].\
                append(f'{zone["ZoneName"]} : {zone["ZoneId"]} : ' +
                       f'{zone["State"]}')

        def default_print(zone_dict):
            for region, zone_list in zone_dict.items():
                print(f'{region} : ')
                for zone in zone_list:
                    print(' ' * 4, end='')
                    print(zone)

        if not pfunc:
            pfunc = default_collect

        if pfunc is default_collect:
            zone_dict = defaultdict(lambda: [])

        try:
            for zone in self.\
                    get_availability_zones():
                pfunc(zone)

            if pfunc is default_collect:
                default_print(zone_dict)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def get_availability_zones(self):
        """Iterate over EC2 availability zones.

        comma separated list of region names.
        """
        for zone in self.ec2_session.get_ec2_client().\
                describe_availability_zones()['AvailabilityZones']:
            yield zone

        return True, None


if __name__ == '__main__':
    pass
