#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Session Manager Class."""

import datetime

from botocore.exceptions import ClientError


class EC2SessionManager():
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

    def get_instances(self, instance_ids=None, project_name=None):
        """Get instances associated with resource.

        Conditionally filter by project name
        and/or instanceIds
        """
        if project_name is None and instance_ids is None:
            return list(self.get_ec2_resource().instances.all())

        if project_name is None and instance_ids is not None:
            return list(self.get_ec2_resource()
                        .instances.filter(InstanceIds=instance_ids.split(',')))

        if project_name is not None:
            filter_config = [{'Name': 'tag:Project', 'Values': [project_name]}]

        if project_name is not None and instance_ids is None:
            return list(self.get_ec2_resource().
                        instances.filter(Filters=filter_config))

        return list(self.get_ec2_resource().
                    instances.filter(Filters=filter,
                                     InstanceIds=instance_ids.split(',')))

    def get_volumes(self, instance_ids=None, project_name=None):
        """Iterate over volumes associated with instances."""
        for inst in self.get_instances(instance_ids, project_name):
            for volume in inst.volumes.all():
                yield inst, volume

    def get_volume_snapshots(self, instance_ids=None, project_name=None):
        """Iterate over snapshots associated with instances and volumes."""
        for inst, volume in self.get_volumes(instance_ids, project_name):
            for snapshot in volume.snapshots.all():
                yield inst, volume, snapshot

    @staticmethod
    def get_instance_tags(instance):
        """Get tags associated with ec2 instance."""
        return {tag['Key']: tag['Value'] for tag in instance.tags or []}

    @staticmethod
    def stop_instance(instance, wait=True, sfunc=None):
        """Stop ec2 instance."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            sfunc(f'Stopping {instance.id}...')

            instance.stop()

            if wait:
                instance.wait_until_stopped()

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot stop {instance.id} : {str(client_err)}'

    @staticmethod
    def start_instance(instance, wait=True, sfunc=None):
        """Start ec2 instance."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if sfunc:
                sfunc(f'Starting {instance.id}...')

            instance.start()

            if wait:
                instance.wait_until_running()

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot start {instance.id} : {str(client_err)}'

    @staticmethod
    def is_instance_running(instance):
        """Determine if the instnace is running or not."""
        if instance.state['Name'] == 'running':
            return True

        return False

    @staticmethod
    def has_pending_volume_snapshots(volume):
        """Check if there are any pending snapshots for this volume."""
        snapshots = list(volume.snapshots.all())
        return snapshots and snapshots[0] == 'pending'

    @staticmethod
    def get_snapshot(volume):
        """Get latest snapshot associated with volume."""
        if volume is None:
            return None

        for snapshot in volume.snapshots.all():
            if snapshot.state == 'completed':
                return snapshot

        return None

    def can_create_volume_snapshot(self, volume, age):
        """Check to see if a volume shanpshot can be created.

        Checks to see if number of days since snapshot
        was created is > age
        """
        if age is None:
            return True

        snapshot = self.get_snapshot(volume)

        if snapshot is None:
            return True

        created_time = snapshot.start_time.now()
        current_time = datetime.datetime.now()
        diff = current_time - created_time

        if diff.days > age:
            return True

        return False

    @staticmethod
    def get_status(success_count, failure_count):
        """Get status helper method."""
        if success_count == 0 and failure_count == 0:
            return False, 'No Instances Selected'

        if success_count > 0 and failure_count == 0:
            return True, 'Success'

        if success_count > 0 and failure_count > 0:
            return False, 'Partial Success'

        return False, 'Failure'

    def get_keypairs(self):
        """Iterate over ec2 keypairs."""
        for keypair in self.get_ec2_resource().key_pairs.all():
            yield keypair


if __name__ == '__main__':
    pass
