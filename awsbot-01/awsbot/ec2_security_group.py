#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Security Group Manager Class."""

from botocore.exceptions import ClientError


class EC2SecurityGroupManager():
    """EC2 Security Group Manager Class."""

    def __init__(self, ec2_session):
        """Initialize the ec2 security group manager class."""
        self.ec2_session = ec2_session

    def list_security_groups(self, long=False, pfunc=None):
        """List All Security Groups In This region."""
        index = 1

        def print_rule(rule_index, rule, spaces=4):
            """Pretty Print rule associated with security group."""
            port = 'Any-Port'
            from_port = rule.get('FromPort', -1)
            if from_port != -1:
                to_port = rule.get('ToPort', -1)
                port = f'{from_port}' if to_port == -1 \
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
                for rule in security_group['IpPermissions']:
                    print_rule(rule_index, rule)
                    rule_index = rule_index + 1

            index = index + 1

        if not pfunc:
            pfunc = default_print

        try:
            for security_group in \
                    self.ec2_session.get_security_groups():
                pfunc(security_group, long)
            return True, None
        except ClientError as client_err:
            return False, client_err


if __name__ == '__main__':
    pass
