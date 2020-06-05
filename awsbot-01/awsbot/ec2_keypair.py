#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 KeyPair Manager Class."""

from botocore.exceptions import ClientError


class EC2KeyPairManager():
    """EC2 KeyPair Manager Class."""

    def __init__(self, ec2_session):
        """Initialize the ec2 keypair manager class."""
        self.ec2_session = ec2_session

    def list_keypairs(self, pfunc=None):
        """List All KeyPairs In This region."""
        index = 1

        def default_print(keypair):
            nonlocal index
            if index == 1:
                print('listing keypairs for : ' +
                      f'{self.ec2_session.session.get_region_name()}')

            print(f'[{index}] : {keypair.meta.data["KeyName"]} - ' +
                  f'{keypair.meta.data["Tags"]}')

            index = index + 1

        if not pfunc:
            pfunc = default_print

        try:
            for keypair in self.ec2_session.get_keypairs():
                pfunc(keypair)
            return True, None
        except ClientError as client_err:
            return False, client_err


if __name__ == '__main__':
    pass
