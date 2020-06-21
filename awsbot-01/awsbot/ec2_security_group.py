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

    def get_ec2_session(self):
        """Get EC2 Session."""
        return self.ec2_session

    def validate_and_get_security_groups(self, groups):
        """Validate one or more security groups passed in.

        groups can be a (comma separated) string or a collection
        of groupids, groupnames or a mix of both.
        """
        if not groups:
            return None, 'No groups specified'

        invalid_groups = set()
        valid_groups = set()
        sg_list = []

        if groups:
            groups, err = util.convert_to_set(groups)
            if not groups:
                return None, err
        else:
            groups = set(groups)

        try:
            for security_group in \
                    self.get_security_groups():
                if security_group['GroupName'] in groups:
                    valid_groups.add(security_group['GroupName'])
                    sg_list.append(security_group)
                elif security_group['GroupId'] in groups:
                    valid_groups.add(security_group['GroupId'])
                    sg_list.append(security_group)
            invalid_groups = groups - valid_groups

            if len(invalid_groups) == 0:
                return sg_list, None

            return None, f'Found Invalid Groups : {invalid_groups}'
        except ClientError as client_err:
            return None, str(client_err)

    def list_security_groups(self, groups=None,
                             long_version=False, pfunc=None):
        """List All Security Groups In This region.

        groups can be a (comma separated) string or a collection
        of groupids, groupnames or a mix of both.
        """
        index = 1

        def get_port_label(port, from_port, to_port):
            if from_port not in (-1, 0, 65535):
                port = f'{from_port}' if to_port in (-1, from_port) \
                    else f'{from_port}-{to_port}'
            return port

        def get_icmp_prot_label(prot, from_port, to_port):
            if from_port == -1:
                prot = prot + '-anycode'
            else:
                prot = prot + '-' + str(from_port)

            if to_port == -1:
                prot = prot + '-anytype'
            else:
                prot = prot + '-' + str(to_port)
            return prot

        def print_rule(rule_index, rule, spaces=4):
            port = 'Any-Port'
            prot = rule.get('IpProtocol', -1)
            if prot != -1:
                from_port = rule.get('FromPort', -1)
                to_port = rule.get('ToPort', -1)
                port = get_port_label(port, from_port, to_port)

            prot = 'Any-Protocol' if prot == '-1' else prot
            if 'icmp' in prot:
                port = 'N/A'
                prot = get_icmp_prot_label(prot, from_port, to_port)

            sub_rule_index = 1
            prefix = f'{prot} | {port} '

            if rule['IpRanges']:
                for cidrip in rule['IpRanges']:
                    print(f'{" " * spaces}[{rule_index}-{sub_rule_index}] ' +
                          f'| {prefix} | {cidrip["CidrIp"]}')
                    sub_rule_index = sub_rule_index + 1

            if rule['Ipv6Ranges']:
                for cidrip in rule['Ipv6Ranges']:
                    print(f'{" " * spaces}[{rule_index}-{sub_rule_index}] ' +
                          f'| {prefix} | {cidrip["CidrIpv6"]}')
                    sub_rule_index = sub_rule_index + 1

            if rule['UserIdGroupPairs']:
                for group in rule['UserIdGroupPairs']:
                    print(f'{" " * spaces}[{rule_index}-{sub_rule_index}] ' +
                          f'| {prefix} | {group["GroupId"]}')
                    sub_rule_index = sub_rule_index + 1

        def default_print(security_group, long_version):
            nonlocal index
            if index == 1:
                print('listing security groups for : ' +
                      f'{self.ec2_session.session.get_region_name()}')

            if long_version:
                print('*' * 80)

            print(f'[{index}] : ' +
                  f'{security_group["GroupId"]} - ' +
                  f'{security_group["VpcId"]} - ' +
                  f'{security_group["GroupName"]} - ' +
                  f'{security_group["Description"]} - ' +
                  f'{security_group.get("Tags", [])}')

            if long_version:
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

        try:
            for security_group in \
                    self.get_security_groups(groups, groups):
                pfunc(security_group, long_version)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def create_security_groups(self, group_names, vpc_ids,
                               descriptions, sfunc=None):
        """Create Security Groups."""
        if not (group_names and vpc_ids):
            return False, 'Require group_names and vpc_ids'

        group_vpc_id_dict, err = \
            util.get_dict_from_list(group_names, vpc_ids,
                                    lambda key, vals: vals[-1], True)
        if err:
            return False, err

        group_descr_dict, err = \
            util.get_dict_from_list(group_names, descriptions,
                                    lambda key, vals:
                                    self.ec2_session.
                                    get_default_description(key))
        if err:
            return False, err

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        try:
            for group_name, vpc_id in group_vpc_id_dict.items():
                aok, err = self.\
                    create_security_group(group_name, vpc_id,
                                          group_descr_dict[group_name],
                                          sfunc)
                if not aok:
                    sfunc(err)
                    failure_count += 1
                else:
                    success_count += 1
            return self.ec2_session.get_status(success_count, failure_count)
        except ClientError as client_err:
            return False, str(client_err)

    def delete_security_groups(self, groups, sfunc=None):
        """Delete Security Groups.

        groups can be a (comma separated) string or a collection
        of groupids, groupnames or a mix of both.
        """
        if not groups:
            return False, 'No groups specified'

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        try:
            for security_group in self.\
                    get_security_groups(groups, groups):
                aok, err = self.\
                        delete_security_group(security_group['GroupId'],
                                              security_group['GroupName'],
                                              sfunc)
                if not aok:
                    sfunc(err)
                    failure_count += 1
                else:
                    success_count += 1
            return self.ec2_session.get_status(success_count, failure_count)
        except ClientError as client_err:
            return False, str(client_err)

    def create_security_group(self, group_name,
                              vpc_id, description=None, sfunc=None):
        """Create a Security Group."""
        if not group_name and not vpc_id:
            return False, 'Require group_name and vpc_id'

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if not description:
                description = self.ec2_session.\
                    get_default_description(group_name)
            sfunc(f'Creating Security Group : {group_name} : {vpc_id}')
            self.ec2_session.\
                get_ec2_resource().\
                create_security_group(Description=description,
                                      GroupName=group_name,
                                      VpcId=vpc_id)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def delete_security_group(self, group_id, group_name, sfunc=None):
        """Delete a Security Group."""
        if not group_id and not group_name:
            return False, 'Require group_id or group_name'

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            sfunc(f'Deleting Security Group : {group_id}' +
                  f'{" : " + group_name if group_name else ""}')

            if group_id:
                self.ec2_session.get_ec2_client().\
                    delete_security_group(GroupId=group_id)
            else:
                self.ec2_session.get_ec2_client().\
                    delete_security_group(GroupName=group_name)

            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    def get_security_groups(self, group_ids=None, group_names=None):
        """Iterate over security groups.

        group ids or group names passed can be a list or a set
        or a comma separated string.
        """
        if group_ids:
            group_ids, err = util.\
                convert_to_list(group_ids, remove_duplicates=True)
            if not group_ids:
                return False, err

        if group_names:
            group_names, err = util.\
                convert_to_list(group_names, remove_duplicates=True)
            if not group_names:
                return False, err

        paginator = \
            self.ec2_session.get_describe_security_groups_paginator()

        for page in paginator.paginate():
            for security_group in page['SecurityGroups']:
                match = False

                if not group_ids and not group_names:
                    match = True

                if not match and group_ids and \
                        security_group['GroupId'] in group_ids:
                    match = True

                if not match and group_names and \
                        security_group['GroupName'] in group_names:
                    match = True

                if match:
                    yield security_group

        return True, None


if __name__ == '__main__':
    pass
