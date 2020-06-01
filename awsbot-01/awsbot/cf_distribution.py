#! /usr/bin/python
# -*- coding:utf8 -*-

"""Cliud Front Distribution Manager class."""

from pprint import pprint
from botocore.exceptions import ClientError


class CFDistributionManager():
    """Cloud front Distribution Manager class."""

    def __init__(self, cf_session):
        """Initialize the cloud front distribution manager class."""
        self.cf_session = cf_session

    def list_all_distributions(self,
                               pfunc=lambda dist:
                               print(f'{dist["ARN"]} : ' +
                                     f'{dist["DomainName"]}')):
        """List All distributions."""
        try:
            for dist in self.cf_session.get_distributions():
                pfunc(dist)
            return None
        except ClientError as client_err:
            return str(client_err)

    def find_distribution(self, domain_name):
        """Find distribution matching domain_name."""
        try:
            for dist in self.cf_session.get_distributions():
                if dist['Aliases']['Quantity'] > 0:
                    for alias in dist['Aliases']['Items']:
                        if alias == domain_name:
                            return dist, None
                if dist['DomainName'] == domain_name:
                    return dist, None
            return None, \
                f'Couldnot Find distribution matching {domain_name}'
        except ClientError as client_err:
            return None, str(client_err)

    def list_distribution(self, domain_name, pfunc=None):
        """List All distributions."""
        def default_print(dist):
            output = {}
            output['ARN'] = dist["ARN"]
            output['DomainName'] = dist["DomainName"]
            output['Origins'] = dist["Origins"]
            output['DefaultCacheBehavior'] = \
                dist["DefaultCacheBehavior"]
            pprint(output)

        if not pfunc:
            pfunc = default_print

        dist, err = self.find_distribution(domain_name)

        if not err:
            pfunc(dist)

        return err

    def create_s3_distribution(self, domain_name, s3_bucket_domain,
                               cert_arn, root_object='index.html'):
        """Create a cloud front distribution for the given s3 bucket domain."""
        try:
            dist = self.cf_session.get_cf_client().\
                create_distribution(
                    DistributionConfig=self.cf_session.
                    create_cf_distribution_config(domain_name,
                                                  s3_bucket_domain,
                                                  cert_arn, root_object))
            return dist['Distribution'], None
        except ClientError as client_err:
            return None, str(client_err)

    def wait_for_distribution_to_be_deployed(self, dist_id):
        """Wait for a distribution to be deployed."""
        try:
            waiter = self.cf_session.get_cf_distribution_deployed_waiter()

            waiter.wait(Id=dist_id,
                        WaiterConfig=self.cf_session.
                        create_cf_waiter_config())
            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
