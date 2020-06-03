#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Session Manager Class."""


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

    def get_instances(self, instance_ids, project_name):
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

    @staticmethod
    def get_instance_tags(instance):
        """Get tags associated with ec2 instance."""
        return {tag['Key']: tag['Value'] for tag in instance.tags or []}


if __name__ == '__main__':
    pass
