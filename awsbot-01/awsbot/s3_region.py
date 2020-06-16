#! usr/bin/python
# -*- coding:utf-8 -*-

"""Utility to get s3 endpoint, zone and region name."""

from collections import namedtuple

try:
    from awsbot import util
except ImportError:
    import util

Endpoint = namedtuple('Endpont', ['name', 'endpoint', 'zone'])


class S3RegionConfig():
    """class to maintain mapping of region names to s3 endpoints and zones."""

    class __S3RegionConfig():
        """singleton class map region names to s3 endpoints."""

        def __init__(self, csvfile='config/region.csv'):
            """Initialize the region_endpoints dictionary."""
            self.region_endpoints = {}
            self.init(csvfile)

        def init(self, csvfile='config/region.csv'):
            """Initialize the region_endpoints dictionary."""
            save = self.region_endpoints
            self.region_endpoints = {}
            aok, err = util.csv_to_dict(csvfile,
                                        self.region_endpoints, Endpoint)
            if not aok:
                self.region_endpoints = save
                raise FileNotFoundError(err)

        def is_valid_region(self, region):
            """Validate region."""
            return region in self.region_endpoints

        def get_endpoint(self, region):
            """Get s3 endpoint associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].endpoint.strip(), None

        def get_region_name(self, region):
            """Get name associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].name.strip(), None

        def get_zone(self, region):
            """Get route53 zone id associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].zone.strip(), None

    instance = None

    def __init__(self, csvfile='config/region.csv'):
        """Initialize the Region singleton class."""
        if not S3RegionConfig.instance:
            S3RegionConfig.instance = \
                 S3RegionConfig.__S3RegionConfig(csvfile)

    def __getattr__(self, name):
        """Delegate getattr requests to the inner class."""
        return getattr(self.instance, name)


if __name__ == '__main__':
    pass
