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
        """List EC2 volume snapshots."""

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

    def create_volume_snapshots(self, instance_ids=None, project_name=None,
                                age=None, sfunc=None,
                                comment='created by awsbot app'):
        """Create EC2 volume snapshots."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            for instance, volume in self.ec2_session.\
                    get_volumes(instance_ids, project_name):
                stopped = False
                if self.ec2_session.has_pending_volume_snapshots(volume):
                    sfunc(f'skipping {volume.id}, '
                          'snapshot already in progress')
                    continue

                if not self.ec2_session.\
                        can_create_volume_snapshot(volume, age):
                    sfunc('skipping snapshot creation for '
                          f'{instance.id}-{volume.id}...snapshot already'
                          f'created in < than {age} days')
                    continue

                if self.ec2_session.is_instance_running(instance):
                    ok, err = self.ec2_session.\
                        stop_instance(instance, True)
                    if ok:
                        stopped = True
                    else:
                        sfunc(err)
                        continue

                sfunc(f'creating snapshot...({instance.id}, {volume.id})')
                volume.create_snapshot(Description=comment)
                if stopped:
                    ok, err = self.ec2_session.start_instance(instance, True)
                    if err:
                        sfunc(err)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
