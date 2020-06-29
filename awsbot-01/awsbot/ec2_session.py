#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Session Manager Class."""

import sys
import datetime

from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class EC2SessionManager():
    """EC2 Session Manager Class."""

    USER_DATA_MIME_HEADER_FILE = 'resources/templates/script/mime_part.sh'
    USER_DATA_MIME_HEADER = None
    INSTANCE_STATES = frozenset({'pending', 'running', 'shutting-down',
                                 'terminated', 'stopping', 'stopped'})

    def __init__(self, session):
        """Initialize the EC2 Session MAnager class."""
        self.session = session
        EC2SessionManager.USER_DATA_MIME_HEADER, err = \
            util.get_file_as_string(self.USER_DATA_MIME_HEADER_FILE)
        if err:
            sys.exit(err)

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

    def get_ec2_paginator(self, name):
        """Get ec2 paginator."""
        try:
            return self.get_ec2_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_describe_security_groups_paginator(self):
        """Get ec2 'DescribeSecurityGroups' paginator."""
        return self.get_ec2_paginator('describe_security_groups')[0]

    def get_describe_iam_instance_profile_associations_paginator(self):
        """Get ec2 'DescribeIamInstanceProfileAssociations' paginator."""
        return self.\
            get_ec2_paginator('describe_iam_instance_profile_associations')[0]

    def get_instances(self, instance_ids=None, project_name=None,
                      states=None, include_states=None):
        """Get instances associated with resource.

        Conditionally filter by project name
        and/or instanceIds

        Also filter by interesting states.
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
        params_dict = {}

        if instance_ids:
            params_dict['InstanceIds'], err = \
                util.str_to_list(instance_ids, remove_duplicates=True)
            if err:
                return None

        if project_name:
            params_dict['Filters'] = \
                [{'Name': 'tag:Project', 'Values': [project_name]}]

        if states and include_states is not None:
            states, err = util.str_to_set(states)
            if err:
                return None
            if not include_states:
                states = self.INSTANCE_STATES - states
            filters = params_dict.get('Filters', [])
            filters.append({'Name': 'instance-state-name',
                            'Values': list(states)})
            params_dict['Filters'] = filters

        if not params_dict:
            return list(self.get_ec2_resource().instances.all())

        return list(self.get_ec2_resource().instances.filter(**params_dict))

    def get_volumes(self, instance_ids=None, project_name=None):
        """Iterate over volumes associated with instances."""
        for inst in self.get_instances(instance_ids, project_name,
                                       states='terminated',
                                       include_states=False):
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
    def terminate_instance(instance, wait=True, sfunc=None):
        """Terminate ec2 instance."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            sfunc(f'Terminating {instance.id}...')

            instance.terminate()

            if wait:
                instance.wait_until_terminated()

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot terminate {instance.id} : {str(client_err)}'

    @staticmethod
    def modify_instance_security_groups(instance,
                                        security_group_id_list=None,
                                        sfunc=None):
        """Modify ec2 instance security groups."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if security_group_id_list:
                sfunc(f'Modifying {instance.id}...' +
                      f'Groups={security_group_id_list}')
                instance.modify_attribute(Groups=security_group_id_list)

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot modify instance {instance.id} : {str(client_err)}'

    @staticmethod
    def modify_instance_src_dest_check_flag(instance,
                                            src_dest_check_flag=None,
                                            sfunc=None):
        """Modify ec2 instance src dest check flag."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if src_dest_check_flag is not None:
                sfunc(f'Modifying {instance.id}...' +
                      f'SourceDestCheck={src_dest_check_flag}')
                instance.modify_attribute(
                    SourceDestCheck={'Value': src_dest_check_flag})

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot modify instance {instance.id} : {str(client_err)}'

    @staticmethod
    def modify_instance_name(instance, instance_name=None, sfunc=None):
        """Modify ec2 instance name."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if instance_name:
                instance.create_tags(
                    Tags=[{'Key': 'Name',
                           'Value': instance_name}])

            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot modify instance {instance.id} : {str(client_err)}'

    @staticmethod
    def modify_instance_user_data(instance, user_data=None,
                                  base64_encode=False, sfunc=None):
        """Modify ec2 instance user data."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if user_data:
                stopped = False
                if EC2SessionManager.is_instance_running(instance):
                    aok, err = \
                        EC2SessionManager.stop_instance(instance, sfunc=sfunc)
                    if aok:
                        stopped = True
                    else:
                        return False, err

                user_data_bytes = EC2SessionManager.\
                    USER_DATA_MIME_HEADER + user_data
                if base64_encode:
                    user_data_bytes = \
                        util.get_base64_encoding(user_data_bytes)
                sfunc(f'Modifying {instance.id}...' +
                      f'UserData={user_data}')
                instance.modify_attribute(
                    UserData={'Value': user_data_bytes})

                if stopped:
                    aok, err = \
                        EC2SessionManager.start_instance(instance, sfunc=sfunc)
                    if err:
                        return False, err
            return True, None
        except ClientError as client_err:
            return False, \
                f'couldnot modify instance {instance.id} : {str(client_err)}'

    def modify_instance_iam_role(self, instance,
                                 iam_instance_profile_arn=None,
                                 attach_iam_role=None, sfunc=None):
        """Modify ec2 instance iam role."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            assoc_id = None
            iam_role_arn = None
            attach_role = False
            detach_role = False
            reattach_orig = False

            for assoc in self.get_ec2_iam_roles(instance.id):
                assoc_id = assoc['AssociationId']
                iam_role_arn = assoc['IamInstanceProfile']['Arn']

            if attach_iam_role and iam_instance_profile_arn and \
                    iam_instance_profile_arn != iam_role_arn:
                attach_role = True
                if assoc_id:
                    detach_role = True
            elif attach_iam_role is False:
                detach_role = True

            if detach_role:
                self.get_ec2_client().\
                    disassociate_iam_instance_profile(
                        AssociationId=assoc_id)
                reattach_orig = True

            if attach_role:
                self.get_ec2_client().\
                    associate_iam_instance_profile(
                        InstanceId=instance.id,
                        IamInstanceProfile={'Arn': iam_instance_profile_arn})

            return True, None
        except ClientError as client_err:
            if reattach_orig:
                self.get_ec2_client().\
                    associate_iam_instance_profile(
                        InstanceId=instance.id,
                        IamInstanceProfile={'Arn': iam_role_arn})
            return False, \
                f'couldnot modify instance {instance.id} : {str(client_err)}'

    def modify_instance(self, instance, security_group_id_list=None,
                        src_dest_check_flag=None, user_data=None,
                        instance_name=None,
                        iam_instance_profile_arn=None,
                        attach_iam_role=None,
                        base64_encode=False,
                        sfunc=None):
        """Modify ec2 instance."""

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        err_list = []
        _, err = self.modify_instance_security_groups(instance,
                                                      security_group_id_list,
                                                      sfunc)
        if err:
            err_list.append(err)

        _, err = self.modify_instance_src_dest_check_flag(instance,
                                                          src_dest_check_flag,
                                                          sfunc)
        if err:
            err_list.append(err)

        _, err = self.modify_instance_name(instance, instance_name, sfunc)
        if err:
            err_list.append(err)

        _, err = self.modify_instance_user_data(instance, user_data,
                                                base64_encode, sfunc)
        if err:
            err_list.append(err)

        _, err = self.modify_instance_iam_role(instance,
                                               iam_instance_profile_arn,
                                               attach_iam_role, sfunc)
        if err:
            err_list.append(err)

        if err_list:
            return False, ' | '.join(err_list)

        return True, None

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
    def get_status(success_count, failure_count,
                   success_msg='Success',
                   failure_msg='Failure',
                   partial_success_msg='Partial Success',
                   noop_msg='No Instances Selected'):
        """Get status helper method."""
        if success_count == 0 and failure_count == 0:
            return False, noop_msg

        if success_count > 0 and failure_count == 0:
            return True, success_msg

        if success_count > 0 and failure_count > 0:
            return False, partial_success_msg

        return False, failure_msg

    def get_keypairs(self):
        """Iterate over ec2 keypairs."""
        for keypair in self.get_ec2_resource().key_pairs.all():
            yield keypair

    @staticmethod
    def get_default_description(key):
        """Get Default Description."""
        return f'{key} created by awsbot on ' + \
               f'{util.get_utcnow_with_tzinfo()}'

    def get_image_id_from_name(self, image_name):
        """Get EC2 Image Id from Image name."""
        if not image_name:
            return None

        image_filter = [{
            'Name': 'name',
            'Values': [image_name]
        }]

        images = list(self.get_ec2_resource().
                      images.filter(Filters=image_filter))

        if not images:
            return None

        return images[0].id

    def get_image_name_from_id(self, image_id):
        """Get EC2 Image name from Image id."""
        if not image_id:
            return None

        image_filter = [{
            'Name': 'image-id',
            'Values': [image_id]
        }]

        images = list(self.get_ec2_resource().
                      images.filter(Filters=image_filter))

        if not images:
            return None

        return images[0].name

    def get_ec2_iam_roles(self, instance_ids=None):
        """Iterate over iam roles."""
        roles_filter = []
        if instance_ids:
            instance_ids, err = \
                util.str_to_list(instance_ids, remove_duplicates=True)
            if err:
                return None

            roles_filter = [{
                'Name': 'instance-id',
                'Values': instance_ids
            }]

        paginator = \
            self.get_describe_iam_instance_profile_associations_paginator()

        for page in paginator.paginate(Filters=roles_filter):
            for assoc in page['IamInstanceProfileAssociations']:
                yield assoc

        return None


if __name__ == '__main__':
    pass
