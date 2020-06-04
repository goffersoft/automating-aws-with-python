#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Volume Manager Class."""

from botocore.exceptions import ClientError


class EC2VolumeManager():
    """EC2 Voume Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 Volume Manager class."""
        self.ec2_session = ec2_session

    def list_volumes(self, instance_ids=None,
                     project_name=None, pfunc=None):
        """List volumes associated with EC2 instances."""
        def default_print(inst, volume):
            tags = self.ec2_session.get_instance_tags(inst)
            print(','.join((
                volume.id,
                inst.id,
                volume.state,
                str(volume.size) + 'GiB',
                volume.encrypted and 'Encrypted' or 'Not Encrypted',
                'Project='+tags.get('Project', '<no-project>'))))

        if not pfunc:
            pfunc = default_print

        try:
            for inst, volume in self.ec2_session.\
                    get_volumes(instance_ids, project_name):
                pfunc(inst, volume)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
