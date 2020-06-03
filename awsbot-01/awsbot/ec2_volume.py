#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Volume Manager Class."""

from botocore.exceptions import ClientError


class EC2VolumeManager():
    """EC2 Voume Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 Volume Manager class."""
        self.ec2_session = ec2_session

    def list_ec2_volumes(self, project_name, instances, pfunc=None):
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
            for inst in self.ec2_session.\
                    get_instances(instances, project_name):
                for volume in inst.volumes.all():
                    pfunc(inst, volume)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
