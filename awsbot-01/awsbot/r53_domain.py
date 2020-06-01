#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Route 53 Domain Manager class."""

from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class R53DomainManager():
    """Route 53 Domain Manager class."""

    def __init__(self, r53_session):
        """Initialize the route 53 session manager class."""
        self.r53_session = r53_session

    def list_hosted_zones(self,
                          pfunc=lambda zone:
                          print(f"{zone['Name']} : {zone['Id']}")):
        """List Hosted Zones."""
        try:
            for zone in self.r53_session.get_hosted_zones():
                pfunc(zone)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def list_resource_record_sets(self, zone, type_filter=None, pfunc=None):
        """List Resource Record Sets."""
        def def_print(rrset):
            output = f"{rrset['Name']} : Type={rrset['Type']} :" +\
                     f" TTL={rrset.get('TTL', 'N/A')}"
            alias = rrset.get('AliasTarget')
            if alias:
                output += f" : Alias {'{'}" +\
                         f"HostedZoneId={alias['HostedZoneId']}" +\
                         f", DNSName={alias['DNSName']}" +\
                         f", EvaluateTargetHealth={''}" +\
                         f"{alias['EvaluateTargetHealth']}" +\
                         f"{'}'}"
            print(output)

        if not pfunc:
            pfunc = def_print

        try:
            for page in self.r53_session.\
                    get_r53_list_record_set_paginator().\
                    paginate(HostedZoneId=zone):
                for rrset in page['ResourceRecordSets']:
                    if type_filter == rrset['Type']:
                        pfunc(rrset)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def find_hosted_zone(self, domain_name):
        """Find hosted zone associated with 'domain_name."""
        for zone in self.r53_session.get_hosted_zones():
            if domain_name.endswith(zone['Name'][:-1]):
                return zone
        return None

    def create_hosted_zone(self, hosted_zone_name):
        """Create hosted zone."""
        zone = self.r53_session.get_r53_client().\
            create_hosted_zone(Name=hosted_zone_name,
                               CallerReference=str(util.getuuid()))
        return zone['HostedZone']

    def create_alias_domain_record(self, domain_name,
                                   alias_zone_id,
                                   alias_dns_name):
        """Create alias record."""
        try:
            hosted_zone_name, err = \
                self.r53_session.\
                get_zone_name_from_domain(domain_name)
            if err:
                return False, err

            zone = self.find_hosted_zone(domain_name) or \
                self.create_hosted_zone(hosted_zone_name)

            change_batch = self.r53_session.\
                create_resource_record_set_config(
                    rrset_domain_name=domain_name,
                    rrset_alias_zone_id=alias_zone_id,
                    rrset_alias_dns_name=alias_dns_name)

            self.r53_session.get_r53_client().\
                change_resource_record_sets(
                    HostedZoneId=zone['Id'],
                    ChangeBatch=change_batch)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def create_s3_domain_record(self, domain_name, bucket_region):
        """Create S3 domain record."""
        if not self.r53_session.get_session().\
                get_region_config().\
                is_valid_region(bucket_region):
            return False, \
                   f'bucket region : {bucket_region} : not supported'

        bucket_zone_id, _ = self.r53_session.get_session().\
            get_region_config().get_zone(bucket_region)
        endpoint, _ = self.r53_session.get_session().\
            get_region_config().get_endpoint(bucket_region)

        return self.create_alias_domain_record(domain_name,
                                               bucket_zone_id,
                                               endpoint)

    def create_cf_domain_record(self, domain_name, cf_domain_name,
                                cf_zone_id=None):
        """Create cloud front domain record."""
        if not cf_zone_id:
            cf_zone_id = self.r53_session.get_default_cf_zone_id()

        return self.create_alias_domain_record(domain_name,
                                               cf_zone_id,
                                               cf_domain_name)


if __name__ == '__main__':
    pass
