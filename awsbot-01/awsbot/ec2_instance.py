#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 instance Manager Class."""

from botocore.exceptions import ClientError

try:
    from awsbot.ec2_security_group import EC2SecurityGroupManager
    from awsbot import util
except ImportError:
    from ec2_security_group import EC2SecurityGroupManager
    import util


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

    def create_instances(self, image_name, instance_type, security_groups,
                         key_name, min_count, max_count, subnet_id,
                         user_data_file, project_name):
        """Create EC2 Instances."""
        if not key_name:
            return False, 'Require key_name'

        if not instance_type:
            return False, 'Require instance_type'

        if not min_count:
            return False, 'Require min_count'

        if not max_count:
            return False, 'Require max_count'

        security_groups, err =\
            EC2SecurityGroupManager(self.ec2_session).\
            validate_and_get_security_groups(security_groups)

        if err:
            return err

        security_groups = [group['GroupId'] for group in security_groups]

        image_id = self.ec2_session.\
            get_image_id_from_name(image_name)

        if not image_id:
            return False, f'Invalid Image Name : {image_name}'

        param_dict = {
            'ImageId': image_id,
            'InstanceType': instance_type,
            'KeyName': key_name,
            'MinCount': min_count,
            'MaxCount': max_count,
            'SecurityGroupIds': security_groups
        }

        if project_name:
            tag_spec = [
                {'ResourceType': 'instance',
                 'Tags': [{
                     'Key': 'Project',
                     'Value': project_name}]},
                {'ResourceType': 'volume',
                 'Tags': [{
                     'Key': 'Project',
                     'Value': project_name}]}
            ]
            param_dict['TagSpecifications'] = tag_spec

        if subnet_id:
            param_dict['SubnetId'] = subnet_id

        if user_data_file:
            user_data_file, err = util.get_file_as_string(user_data_file)
            if err:
                return err
            param_dict['UserData'] = user_data_file

        try:
            instances = self.ec2_session.get_ec2_resource().\
                create_instances(**param_dict)

            return True, 'Success : InstanceIds : ' + \
                f'{[instance.id for instance in instances]}'
        except ClientError as client_error:
            return False, str(client_error)

    def terminate_instances(self, instances=None,
                            project_name=None, sfunc=None):
        """Delete EC2 Instances."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        for inst in self.ec2_session.\
                get_instances(instances, project_name):
            aok, err = self.ec2_session.terminate_instance(inst, False, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

        return self.ec2_session.get_status(success_count, failure_count)


if __name__ == '__main__':
    pass
