#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 instance Manager Class."""

from botocore.exceptions import ClientError


class EC2InstanceManager():
    """EC2 instance Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 instance Manager Class."""
        self.ec2_session = ec2_session

    def list_instances(self, instance_ids=None,
                       project_name=None, pfunc=None):
        """Get instances associated with resource.

        Conditionally filter by project name
        and/or instanceIds
        """
        def default_print(inst):
            tags = self.ec2_session.get_instance_tags(inst)
            print(','.join((inst.id,
                            inst.instance_type,
                            inst.public_dns_name,
                            inst.placement['AvailabilityZone'],
                            inst.state['Name'],
                            'Project='+tags.get('Project', '<no-project>'))))

        if not pfunc:
            pfunc = default_print

        try:
            for inst in self.ec2_session.\
                    get_instances(instance_ids, project_name):
                pfunc(inst)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def start_instances(self, instance_ids=None,
                        project_name=None, sfunc=None):
        """Start EC2 instances."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        for inst in self.ec2_session.\
                get_instances(instance_ids, project_name):
            aok, err = self.ec2_session.start_instance(inst, False, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

        return self.ec2_session.get_status(success_count, failure_count)

    def stop_instances(self, instance_ids=None,
                       project_name=None, sfunc=None):
        """Stop EC2 instances."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        for inst in self.ec2_session.\
                get_instances(instance_ids, project_name):
            aok, err = self.ec2_session.stop_instance(inst, False, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

        return self.ec2_session.get_status(success_count, failure_count)

    def reboot_instances(self, instance_ids=None,
                         project_name=None, sfunc=None):
        """Reboot EC2 Instances."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        for inst in self.ec2_session.\
                get_instances(instance_ids, project_name):
            aok, err = self.ec2_session.stop_instance(inst, True, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

            aok, err = self.ec2_session.start_instance(inst, False, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

        return self.ec2_session.get_status(success_count, failure_count)


if __name__ == '__main__':
    pass
