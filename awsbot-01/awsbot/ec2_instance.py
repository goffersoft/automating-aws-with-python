#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 instance Manager Class."""

from botocore.exceptions import ClientError


class EC2InstanceManager():
    """EC2 instance Manager Class."""

    def __init__(self, ec2_session):
        """Initialize EC2 instance Manager Class."""
        self.ec2_session = ec2_session

    def list_instances(self, instances, project_name, pfunc=None):
        """Get instances associated with resource.

        Conditionally filter by project name
        and/or instanceIds
        """
        def default_print(inst):
            tags = {tag['Key']: tag['Value'] for tag in inst.tags or []}
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
                    get_instances(instances, project_name):
                pfunc(inst)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    @staticmethod
    def stop_ec2_instance(instance, wait,
                          pfunc=lambda inst:
                          print('Stopping {0}...'.format(inst.id))):
        """Stop ec2 instance."""
        try:
            if pfunc:
                pfunc(instance)

            instance.stop()

            if wait:
                instance.wait_until_stopped()

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot stop {instance.id} : {str(client_err)}'

    @staticmethod
    def start_ec2_instance(instance, wait,
                           pfunc=lambda inst:
                           print('Starting {0}...'.format(inst.id))):
        """Start ec2 instance."""
        try:
            if pfunc:
                pfunc(instance)

            instance.start()

            if wait:
                instance.wait_until_running()

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot start {instance.id} : {str(client_err)}'

    def start_ec2_instances(self, instances, project_name):
        """Start EC2 instances."""
        err_list = []
        ret_val = False
        for inst in self.ec2_session.\
                get_instances(instances, project_name):
            ok, err = self.start_ec2_instance(inst, False)
            if not ok:
                err_list.append(err)
            else:
                ret_val = True

        if not ret_val and not err_list:
            return False, 'No Instances Selected'

        return ret_val, err_list

    def stop_ec2_instances(self, instances, project_name):
        """Stop EC2 instances."""
        err_list = []
        ret_val = False
        for inst in self.ec2_session.\
                get_instances(instances, project_name):
            ok, err = self.stop_ec2_instance(inst, False)
            if not ok:
                err_list.append(err)
            else:
                ret_val = True

        if not ret_val and not err_list:
            return False, 'No Instances Selected'

        return ret_val, err_list


if __name__ == '__main__':
    pass
