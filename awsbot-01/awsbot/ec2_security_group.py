#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Security Group Manager Class."""

from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class EC2SecurityGroupManager():
    """EC2 Security Group Manager Class."""

    def __init__(self, ec2_session):
        """Initialize the ec2 security group manager class."""
        self.ec2_session = ec2_session

    def list_security_groups(self, group_ids=None, group_names=None,
                             long=False, pfunc=None):
        """List All Security Groups In This region."""
        index = 1

        def print_rule(rule_index, rule, spaces=4):
            port = 'Any-Port'
            from_port = rule.get('FromPort', -1)
            if from_port != -1:
                to_port = rule.get('ToPort', -1)
                port = f'{from_port}' if to_port == -1 \
                    or from_port == to_port \
                    else f'{from_port}-{to_port}'
            prot = rule.get('IpProtocol', -1)
            prot = 'Any-Protocol' if prot == '-1' else prot

            print(f'{" " * spaces}[{rule_index}] ' +
                  f': {port} : {prot} : ', end='')
            if not rule['UserIdGroupPairs']:
                print(f'{rule["IpRanges"]} : {rule["Ipv6Ranges"]}')
            else:
                group_ids = [group['GroupId'] for group
                             in rule["UserIdGroupPairs"]]
                print(f'{group_ids}')

        def default_print(security_group, long):
            nonlocal index
            if index == 1:
                print('listing security groups for : ' +
                      f'{self.ec2_session.session.get_region_name()}')

            if long:
                print('*' * 80)

            print(f'[{index}] : ' +
                  f'{security_group["GroupId"]} - ' +
                  f'{security_group["VpcId"]} - ' +
                  f'{security_group["GroupName"]} - ' +
                  f'{security_group["Description"]} - ' +
                  f'{security_group.get("Tags", [])}')

            if long:
                rule_index = 1
                print()
                print('    Ingress-Rules')
                for rule in security_group['IpPermissions']:
                    print_rule(rule_index, rule)
                    rule_index = rule_index + 1

                rule_index = 1
                print()
                print('    Egress-Rules')
                for rule in security_group['IpPermissionsEgress']:
                    print_rule(rule_index, rule)
                    rule_index = rule_index + 1

            index = index + 1

        if not pfunc:
            pfunc = default_print

        group_id_list = None
        group_name_list = None

        if group_ids:
            group_id_list = util.str_to_list(group_ids)

        if group_names:
            group_name_list = util.str_to_list(group_names)

        try:
            for security_group in \
                    self.ec2_session.get_security_groups(group_id_list,
                                                         group_name_list):
                pfunc(security_group, long)
            return True, None
        except ClientError as client_err:
            return False, client_err

    def create_security_group(self, group_name,
                              vpc_id, description=None):
        """Create a Security Group."""
        try:
            if not description:
                description = self.ec2_session.\
                    get_default_security_group_description(group_name)
            self.ec2_session.\
                get_ec2_resource().\
                create_security_group(Description=description,
                                      GroupName=group_name,
                                      VpcId=vpc_id)
            return True, None
        except ClientError as client_err:
            return False, client_err

    def delete_security_groups(self, group_ids, group_names, sfunc=None):
        """Delete Security Groups."""
        if not group_ids and not group_names:
            return False, 'Require group_names or group_ids'

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        group_id_list = None
        group_name_list = None

        if group_ids:
            group_id_list = util.str_to_list(group_ids)

        if group_names:
            group_name_list = util.str_to_list(group_names)

        success_count = 0
        failure_count = 0
        try:
            for security_group in self.ec2_session.\
                    get_security_groups(group_id_list,
                                        group_name_list):
                ok, err = self.ec2_session.\
                        delete_security_group(security_group['GroupId'],
                                              None, sfunc)
                if not ok:
                    sfunc(err)
                    failure_count += 1
                else:
                    success_count += 1
            return self.ec2_session.get_status(success_count, failure_count)
        except ClientError as client_err:
            return False, client_err


if __name__ == '__main__':
    pass
