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
                       project_name=None, states=None,
                       include_states=None, pfunc=None):
        """Get instances associated with resource.

        Conditionally filter by project name
        and/or instanceIds
        Also filter by intersting states.
        include_states = None => list all instances
                                 regardless of state.
        include_states = True => list all instances
                                 whose state matches
                                 any state in the states
                                 variable.
        include_states = False => list all instances
                                  whose state doesnot match
                                  any state in the states
                                  variable.
        """
        def default_print(inst):
            print()
            print(f'{80 * "*"}')
            print()

            tags = self.ec2_session.get_instance_tags(inst)
            image_name = self.ec2_session.get_image_name_from_id(inst.image_id)
            security_group_names = \
                ', '.join([sg['GroupName'] for sg in inst.security_groups])
            sd_check = 'SourceDestCheck Enabled' \
                if inst.source_dest_check \
                else 'SourceDestCheck Disabled'
            public_ip = 'N/A' \
                if not inst.public_ip_address \
                else inst.public_ip_address
            private_ip = 'N/A' \
                if not inst.private_ip_address \
                else inst.private_ip_address
            private_dns = 'N/A' \
                if not inst.private_dns_name \
                else inst.private_dns_name
            public_dns = 'N/A' \
                if not inst.public_dns_name \
                else inst.public_dns_name
            instance_name = tags.get('Name', 'N/A')
            vpc_id = 'N/A' if not inst.vpc_id else inst.vpc_id

            print(' | '.join((inst.id,
                              instance_name,
                              inst.image_id,
                              image_name,
                              inst.instance_type,
                              public_ip,
                              private_ip,
                              public_dns,
                              private_dns,
                              inst.key_name,
                              vpc_id,
                              inst.placement['AvailabilityZone'],
                              security_group_names,
                              sd_check,
                              inst.state['Name'],
                              'Project='+tags.get('Project', '<no-project>'))))

        if not pfunc:
            pfunc = default_print

        try:
            for inst in self.ec2_session.\
                    get_instances(instance_ids, project_name,
                                  states, include_states):
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
                get_instances(instance_ids, project_name,
                              states='terminated', include_states=False):
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
                get_instances(instance_ids, project_name,
                              states='terminated', include_states=False):
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
                get_instances(instance_ids, project_name,
                              states='terminated', include_states=False):
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
                         user_data, user_data_file,
                         project_name, instance_name):
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

        if instance_name:
            min_count = 1
            max_count = 1

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

        if instance_name:
            instance_name_tag_dict = \
                {'Key': 'Name', 'Value': instance_name}
            tag_spec = param_dict.get('TagSpecifications', [])
            tags = None
            for tag in tag_spec:
                if tag['ResourceType'] == 'instance':
                    tags = tag['Tags']
                    break

            if not tags:
                tags = []
                tag_spec.append({'ResourceType': 'instance', 'Tags': tags})

            tags.append(instance_name_tag_dict)
            param_dict['TagSpecifications'] = tag_spec

        if subnet_id:
            param_dict['SubnetId'] = subnet_id

        if user_data:
            user_data_file, err = self.\
                get_user_data_as_string(user_data_file)
            user_data_file = self.update_user_data(user_data_file,
                                                   instance_name)
            if err:
                return False, err

            param_dict['UserData'] = \
                util.get_base64_encoding(user_data_file)

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
                get_instances(instances, project_name,
                              states='terminated', include_states=False):
            aok, err = self.ec2_session.terminate_instance(inst, False, sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

        return self.ec2_session.get_status(success_count, failure_count)

    def modify_instances(self, instances, security_groups,
                         source_dest_check_flag,
                         user_data, user_data_file,
                         project_name=None, instance_names=None,
                         sfunc=None):
        """Modify EC2 Instances."""
        if security_groups:
            security_groups, err =\
                EC2SecurityGroupManager(self.ec2_session).\
                validate_and_get_security_groups(security_groups)

            if err:
                return err

            security_groups = [group['GroupId'] for group in security_groups]

        if user_data:
            user_data_file, err = self.\
                get_user_data_as_string(user_data_file)
            if err:
                return False, err

        if instance_names:
            instance_names, err = util.convert_to_list(instance_names)
            if not instance_names:
                return False, err

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        index = 0
        for inst in self.ec2_session.\
                get_instances(instances, project_name,
                              states='terminated', include_states=False):
            instance_name = None \
                if not instance_names or index >= len(instance_names) \
                else instance_names[index]
            if not instance_name:
                tags = self.ec2_session.get_instance_tags(inst)
                instance_name = tags.get('Name')
            if user_data:
                user_data_file = self.update_user_data(user_data_file,
                                                       instance_name)
            aok, err = self.\
                ec2_session.modify_instance(inst, security_groups,
                                            source_dest_check_flag,
                                            user_data_file, instance_name,
                                            sfunc)
            if not aok:
                sfunc(err)
                failure_count += 1
            else:
                success_count += 1

            index += 1

        return self.ec2_session.get_status(success_count, failure_count)

    @staticmethod
    def get_user_data_as_string(user_data_file):
        """Get user data as String."""
        if not user_data_file:
            return None, 'Require valid path to user data file'

        user_data, err = util.get_file_as_string(user_data_file)
        if err:
            return None, err

        return user_data, None

    @staticmethod
    def update_user_data(user_data, instance_name):
        """Update user data string with instance specific attributes."""
        if user_data.find('%s') != -1:
            if instance_name:
                user_data %= instance_name
            else:
                user_data = ''.join(user_data.split('%s'))

        return user_data


if __name__ == '__main__':
    pass
