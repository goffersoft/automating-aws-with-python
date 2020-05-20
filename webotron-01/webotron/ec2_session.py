#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Session Manager Class."""


class Ec2SessionManager():
    """EC2 Session Manager Class."""

    def __init__(self, session):
        """Initialize the EC2 Session MAnager class."""
        self.session = session

    def get_ec2_resource(self):
        """Get ec2 resource."""
        return self.session.get_resource('ec2')

    def get_ec2_client(self):
        """Get ec2 client."""
        return self.session.get_client('ec2')

    def get_session(self):
        """Get session."""
        return self.session

    def set_session(self, session):
        """Set session."""
        self.session = session



if __name__ == '__main__':
    pass
