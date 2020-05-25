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

    def get_hosted_zones(self):
        """Get route 53 client."""
        return self.get_r53_client().list_hosted_zones_by_name()


if __name__ == '__main__':
    pass
