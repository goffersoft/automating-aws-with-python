#! usr/bin/python
# -*- coding:utf-8 -*-

"""Utility to get s3 endpoint, zone and region name."""

from collections import namedtuple

try:
    import util
except ModuleNotFoundError:
    from . import util

Endpoint = namedtuple('Endpont', ['name', 'endpoint', 'zone'])


class Region():
    """class to maintain mapping of region names to s3 endpoints and zones."""

    class __Region():
        """singleton class map region names to s3 endpoints."""

        def __init__(self, csvfile='config/region.csv'):
            """Initialize the region_endpoints dictionary."""
            self.region_endpoints = {}
            self.init(csvfile)

        def init(self, csvfile='config/region.csv'):
            """Initialize the region_endpoints dictionary."""
            save = self.region_endpoints
            self.region_endpoints = {}
            ok, err = util.csv_to_dict(csvfile,
                                       self.region_endpoints, Endpoint)
            if not ok:
                self.region_endpoints = save
                raise FileNotFoundError(err)

        def is_valid_region(self, region):
            """Validate region."""
            return region in self.region_endpoints

        def get_endpoint(self, region):
            """Get s3 endpoint associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].endpoint, None

        def get_region_name(self, region):
            """Get name associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].name, None

        def get_zone(self, region):
            """Get route53 zone id associated with region."""
            if not self.is_valid_region(region):
                return None, f'Invalid Region : {region}'

            return self.region_endpoints[region].zone, None

    instance = None

    def __init__(self, csvfile='config/region.csv'):
        """Initialize the Region singleton class."""
        if not Region.instance:
            Region.instance = Region.__Region(csvfile)

    def __getattr__(self, name):
        """Delegate getattr requests to the inner class."""
        return getattr(self.instance, name)

    @classmethod
    def init(cls, csvfile='config/region.csv'):
        """Re-Initialize the singleton class with new config."""
        cls.instance.init(csvfile)


if __name__ == '__main__':
    pass
