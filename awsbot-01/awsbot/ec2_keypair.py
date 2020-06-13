#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 KeyPair Manager Class."""

import stat
from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


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

    def is_already_created(self, keypair_name):
        """Determine if the KeyPair has already been created."""
        try:
            for keypair in self.ec2_session.get_keypairs():
                if keypair_name == keypair.name:
                    return True, keypair, None
            return False, None, None
        except ClientError as client_err:
            return False, None, str(client_err)

    def create_keypair(self, keypair_name, output_filepath):
        """Create a KeyPair."""
        aok, path = util.is_valid_file_path(output_filepath)

        if not aok:
            return False, f'Invalid file path : {output_filepath}'

        aok, _, err = self.is_already_created(keypair_name)
        if err:
            return False, err

        if aok:
            return False, f'keypair : {keypair_name} : already exists'

        keypair = None
        try:
            keypair = self.ec2_session.get_ec2_resource().\
                          create_key_pair(KeyName=keypair_name)
        except ClientError as client_err:
            return False, str(client_err)

        with path.open('w') as pem_file:
            pem_file.write(keypair.key_material)

        path.chmod(stat.S_IRUSR | stat.S_IWUSR)

        return True, None

    def delete_keypair(self, keypair_name):
        """Delete a KeyPair."""
        aok, keypair, err = self.is_already_created(keypair_name)
        if err:
            return False, err

        if not aok:
            return False, f'keypair : {keypair_name} : doesnot exist'

        try:
            keypair.delete()
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def import_keypair(self, keypair_name, public_key_file):
        """Import a KeyPair."""
        aok, path = util.does_file_exist(public_key_file)

        if not aok:
            return False, f'Invalid public key file: {public_key_file}'

        aok, _, err = self.is_already_created(keypair_name)
        if err:
            return False, err

        if aok:
            return False, f'keypair : {keypair_name} : already exists'

        public_key_bytes = None
        with path.open('rb') as key_file:
            public_key_bytes = key_file.read()

        try:
            self.ec2_session.get_ec2_resource().\
                      import_key_pair(KeyName=keypair_name,
                                      PublicKeyMaterial=public_key_bytes)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
