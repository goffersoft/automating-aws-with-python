#! usr/bin/python
# -*- coding:utf-8 -*-

"""Utility to get s3 endpoint, zone and region name."""

from collections import namedtuple

import util

g_region_endpoints = {}
Endpoint = namedtuple('Endpont', ['name', 'endpoint', 'zone'])


def is_valid_region(region):
    """Validate region."""
    return region in g_region_endpoints


def get_endpoint(region):
    """Get s3 endpoint associated with region."""
    if not is_valid_region(region):
        return None, f'Invalid Region : {region}'

    return g_region_endpoints[region].endpoint


def get_region_name(region):
    """Get name associated with region."""
    if not is_valid_region(region):
        return None, f'Invalid Region : {region}'

    return g_region_endpoints[region].name


def get_zone(region):
    """Get route53 zone id associated with region."""
    if not is_valid_region(region):
        return None, f'Invalid Region : {region}'

    return g_region_endpoints[region].zone


def init(csvfile='config/region.csv'):
    """Initialize the region_endpoints dictionary."""
    global g_region_endpoints
    return util.csv_to_dict(csvfile, g_region_endpoints, Endpoint)


if __name__ == '__main__':
    pass
