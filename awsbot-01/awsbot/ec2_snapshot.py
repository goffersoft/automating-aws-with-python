#! /usr/bin/python
# -*- coding:utf-8 -*-


"""EC2 snapshot Manager Class."""

from botocore.exceptions import ClientError


class EC2SnapshotManager():
    """EC2 snapshot Manager Class."""

    def __init__(self, ec2_session):
        """Initialize the EC2 snapshot Manager Class."""
        self.ec2_session = ec2_session

    def list_volume_snapshots(self, instance_ids, project_name,
                              list_all, pfunc=None):
        """List EC2 snapshots."""

        def default_print(inst, volume, snapshot):
            tags = self.ec2_session.get_instance_tags(inst)
            print(','.join((
                snapshot.id,
                volume.id,
                inst.id,
                snapshot.state,
                snapshot.progress,
                snapshot.start_time.strftime('%c'),
                'Project='+tags.get('Project', '<no-project>'))))

        if not pfunc:
            pfunc = default_print

        try:
            skip_volume = None
            for inst, volume, snapshot in self.ec2_session.\
                    get_volume_snapshots(instance_ids, project_name):
                if skip_volume and skip_volume == volume:
                    continue
                if skip_volume != volume:
                    skip_volume = None
                pfunc(inst, volume, snapshot)
                if(snapshot.state == 'completed' and not list_all):
                    skip_volume = volume

            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
