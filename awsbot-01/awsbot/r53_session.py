#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Route 53 Session Manager class."""


class R53SessionManager():
    """Route 53 Session Manager class."""

    def __init__(self, session):
        """Initialize the route 53 session manager class."""
        self.session = session

    def get_r53_client(self):
        """Get route 53 client."""
        return self.session.get_client('route53')

    def get_session(self):
        """Get session."""
        return self.session

    def set_session(self, session):
        """Set session."""
        self.session = session

    def get_r53_paginator(self, name):
        """Get route 53 paginator."""
        try:
            return self.get_r53_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_r53_list_record_set_paginator(self):
        """Get route 53 'list_resource_record_sets' paginator."""
        return self.get_r53_paginator('list_resource_record_sets')[0]

    def get_r53_list_hosted_zones_paginator(self):
        """Get route 53 'list_resource_record_sets' paginator."""
        return self.get_r53_paginator('list_hosted_zones')[0]

    def get_hosted_zones(self):
        """Iterate over Hosted Zones."""
        for page in self.\
            get_r53_list_hosted_zones_paginator().\
                paginate():
            for zone in page['HostedZones']:
                yield zone

    @staticmethod
    def get_zone_name_from_domain(domain_name):
        """Get zone name from domain name."""
        domain_parts = domain_name.split('.')
        if len(domain_parts) < 2:
            return None, 'Invalid domain name'

        return '.'.join(domain_parts[-2:]) + '.', None

    @staticmethod
    def create_resource_record_set_config(
            comment='Created By awsbot',
            action='UPSERT',
            rrset_domain_name=None,
            rrset_type='A',
            rrset_alias_zone_id=None,
            rrset_alias_dns_name=None,
            rrset_alias_eval_target_health=False):
        """Create the json blob for resource record set config."""
        return {'Comment': comment,
                'Changes': [{
                    'Action': action,
                    'ResourceRecordSet': {
                        'Name': rrset_domain_name,
                        'Type': rrset_type,
                        'AliasTarget': {
                            'HostedZoneId': rrset_alias_zone_id,
                            'DNSName': rrset_alias_dns_name,
                            'EvaluateTargetHealth':
                            rrset_alias_eval_target_health,
                        }}}]}


if __name__ == '__main__':
    pass
