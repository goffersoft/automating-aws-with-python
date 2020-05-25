#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Route 53 Domain Manager class."""

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


if __name__ == '__main__':
    pass
