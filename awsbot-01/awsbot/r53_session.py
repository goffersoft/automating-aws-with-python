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

    def get_r53_paginator(self, name):
        """Get route 53 paginator."""
        try:
            return self.get_r53_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_r53_list_record_set_paginator(self):
        """Get route 53 'list_resource_record_sets' paginator."""
        return self.get_r53_paginator('list_resource_record_sets')[0]


if __name__ == '__main__':
    pass
