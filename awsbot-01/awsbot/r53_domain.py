#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Route 53 Domain Manager class."""

from botocore.exceptions import ClientError

try:
    from awsbot.session import SessionManager
except ImportError:
    from session import SessionManager


class R53DomainManager():
    """Route 53 Domain Manager class."""

    def __init__(self, r53_session):
        """Initialize the route 53 session manager class."""
        self.r53_session = r53_session

    def list_hosted_zones(self,
                          pfunc=lambda zone:
                          print(f"{zone['Name']} : {zone['Id']}")):
        """List Hosted Zones."""
        response = self.r53_session.get_hosted_zones()

        err, rcode = SessionManager.is_error_response(response)

        if err:
            raise ConnectionError(f'received error response : \
                                    response : {str(response)}')

        for zone in response['HostedZones']:
            pfunc(zone)

    def list_resource_record_sets(self, zone, type_filter=None, pfunc=None):
        """List Resource Record Sets."""
        def def_print(record_set):
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


if __name__ == '__main__':
    pass
