#! /usr/bin/python
# -*- coding:utf:8 -*-

"""EC2 Security Group Rule Manager Class."""

from collections import defaultdict
from botocore.exceptions import ClientError

try:
    from awsbot import util
except ImportError:
    import util


class EC2SecurityGroupRuleManager():
    """EC2 Security Group Rule Manager Class."""

    ip_protocol_list = ('tcp', 'udp', 'icmp', 'icmpv6', 'any')

    def __init__(self, ec2_sg_manager):
        """Initialize the Security Group Rule Manager Class."""
        self.ec2_sg_manager = ec2_sg_manager

    @staticmethod
    def create_security_group_json(groups, group_descriptions,
                                   group_resources,
                                   default_descr_func):
        """Create a Security Group Json Blob."""
        sg_descr_dict, err = \
            util.get_dict_from_list(groups,
                                    group_descriptions,
                                    default_descr_func)
        if err:
            return None, err

        sg_list = []
        for group_name_or_id, descr in sg_descr_dict.items():
            sg_dict = {}
            group_res = None
            for group_res in group_resources:
                if group_name_or_id in \
                        (group_res['GroupId'], group_res['GroupName']):
                    break
            if not group_res:
                return None, 'Internal Error - group_res is None'
            sg_dict['GroupId'] = group_res['GroupId']
            sg_dict['VpcId'] = group_res['VpcId']
            if descr:
                sg_dict['Description'] = descr
            sg_list.append(sg_dict)

        return sg_list, None

    @staticmethod
    def create_ip_cidr_json(ip_cidr, ip_descriptions,
                            default_descr_func,
                            cidr_label):
        """Create a IpCidr Json Blob."""
        ip_cidr_dict, err = \
            util.get_dict_from_list(ip_cidr,
                                    ip_descriptions,
                                    default_descr_func)
        if err:
            return None, err

        ip_list = []
        for ipcidr, descr in ip_cidr_dict.items():
            ip_dict = {}
            ip_dict[cidr_label] = ipcidr
            if descr:
                ip_dict['Description'] = descr
            ip_list.append(ip_dict)

        return ip_list, None

    def create_security_group_rule_json(
            self, ip_protocol='any',
            from_port=None, to_port=None,
            ipv4_cidr='0.0.0.0/0', ipv4_descriptions=None,
            ipv6_cidr='::/0', ipv6_descriptions=None,
            groups=None,
            group_descriptions=None,
            group_resources=None,
            icmp_type=None, icmp_code=None):
        """Create a Json Rule Blob."""
        def default_descr_func(key, vals):
            self.ec2_sg_manager.get_ec2_session().get_default_description(key)

        rule_json = {}
        if ip_protocol == 'any':
            rule_json['IpProtocol'] = '-1'
        else:
            rule_json['IpProtocol'] = ip_protocol

        if 'icmp' in ip_protocol:
            rule_json['FromPort'] = icmp_type if icmp_type != 'any' else -1
            rule_json['ToPort'] = icmp_code if icmp_code != 'any' else -1
        elif ip_protocol != 'any':
            if from_port:
                rule_json['FromPort'] = from_port
            if to_port:
                rule_json['ToPort'] = to_port

        if ipv4_cidr:
            ipv4_list, err = self.\
                create_ip_cidr_json(ipv4_cidr, ipv4_descriptions,
                                    default_descr_func, 'CidrIp')
            if err:
                return None, err
            rule_json['IpRanges'] = ipv4_list

        if ipv6_cidr:
            ipv6_list, err = self.\
                create_ip_cidr_json(ipv6_cidr, ipv6_descriptions,
                                    default_descr_func, 'CidrIpv6')
            if err:
                return None, err
            rule_json['Ipv6Ranges'] = ipv6_list

        if groups:
            sg_list, err = \
                self.create_security_group_json(groups, group_descriptions,
                                                group_resources,
                                                default_descr_func)
            if err:
                return None, err

            rule_json['UserIdGroupPairs'] = sg_list

        return [rule_json], None

    def create_rule(self, groups,
                    egress_rule, ip_protocol='any',
                    from_port=None, to_port=None,
                    ipv4_cidr='0.0.0.0/0', ipv4_descriptions=None,
                    ipv6_cidr='::/0', ipv6_descriptions=None,
                    security_groups=None,
                    security_group_descriptions=None,
                    icmp_type=None, icmp_code=None,
                    sfunc=None):
        """Create a Rule.

        groups can be a (comma separated) string or a collection
        of groupids, groupnames or a mix of both.
        """
        if not groups:
            return False, 'No groups specified'

        groups, err = self.ec2_sg_manager.\
            validate_and_get_security_groups(groups)
        if not groups:
            return False, err

        if ip_protocol not in self.ip_protocol_list:
            return False, f'Invalid ip_protocol : {ip_protocol}'

        if security_groups:
            security_group_resources, err = self.ec2_sg_manager.\
                validate_and_get_security_groups(security_groups)
            if not security_group_resources:
                return False, err

        aok, from_port, to_port = \
            util.validate_range(from_port, to_port)
        if not aok:
            return False, f'Invalid Network Ports : {from_port}-{to_port}'

        rule_json, err = \
            self.create_security_group_rule_json(
                ip_protocol,
                from_port, to_port,
                ipv4_cidr, ipv4_descriptions,
                ipv6_cidr, ipv6_descriptions,
                security_groups,
                security_group_descriptions,
                security_group_resources,
                icmp_type, icmp_code)

        if not aok:
            return False, err

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        success_count = 0
        failure_count = 0
        try:
            for group in groups:
                security_group = \
                    self.ec2_sg_manager.get_ec2_session().\
                    get_ec2_resource().\
                    SecurityGroup(group['GroupId'])
                _, err = self.\
                    create_security_group_rule(
                        security_group, rule_json,
                        egress_rule, sfunc)
                if err:
                    failure_count += 1
                    sfunc(err)
                else:
                    success_count += 1

            return self.ec2_sg_manager.get_ec2_session().\
                get_status(success_count, failure_count)
        except ClientError as client_err:
            return False, str(client_err)

    @staticmethod
    def ignore_field(field, ignore_label='ignore'):
        """Determine if a field can be ignored."""
        if not field or field == ignore_label:
            return True
        return False

    @staticmethod
    def get_rule_json(security_group, egress_rule):
        """Get Rule Json Blob."""
        if egress_rule:
            return security_group['IpPermissionsEgress']
        return security_group['IpPermissions']

    def match_port(self, rule, port_label, port_field, icmp_field):
        """Determine if rule matches the specified port values."""
        if self.ignore_field(port_field) and \
                self.ignore_field(icmp_field):
            return True

        if not self.ignore_field(icmp_field) and \
                'icmp' in rule['IpProtocol'] and \
                rule.get(port_label) and \
                rule[port_label] == icmp_field:
            return True

        if not self.ignore_field(port_field) and \
                'icmp' not in rule['IpProtocol'] and \
                rule.get(port_label) and \
                rule[port_label] == port_field:
            return True

        return False

    def match_list(self, rule, list_label, key_labels, field_list):
        """Determine if rule matches the list of value passed in."""
        if self.ignore_field(field_list):
            return rule[list_label]

        output_list = []
        if not self.ignore_field(field_list) and \
                rule[list_label]:
            for dict_type in rule[list_label]:
                for key in key_labels:
                    if dict_type.get(key) and \
                            dict_type.get(key) in field_list:
                        output_list.append(dict_type)
                        break
        return output_list

    def match_rule(self, rule, ip_protocol=None,
                   from_port=None, to_port=None,
                   ipv4_cidr=None,
                   ipv6_cidr=None,
                   security_groups=None,
                   icmp_type=None, icmp_code=None):
        """Determine if the input fields matches a rule."""
        if not rule:
            return False, None

        match = False

        match = not self.ignore_field(ip_protocol) and \
            rule.get('IpProtocol') and \
            rule['IpProtocol'] == ip_protocol

        match = self.match_port(rule, 'FromPort',
                                from_port, icmp_type)

        match = self.match_port(rule, 'ToPort',
                                to_port, icmp_code)

        if not match:
            return False, None

        ipv4_cidr_list = self.match_list(rule, 'IpRanges',
                                         ('CidrIp',), ipv4_cidr)
        ipv6_cidr_list = self.match_list(rule, 'Ipv6Ranges',
                                         ('CidrIpv6',), ipv6_cidr)
        sg_list = self.match_list(rule, 'UserIdGroupPairs',
                                  ('GroupId', 'GroupName'),
                                  security_groups)

        if not (ipv4_cidr_list or ipv6_cidr_list or sg_list):
            return False, None

        rule['IpRanges'] = ipv4_cidr_list
        rule['Ipv6Ranges'] = ipv6_cidr_list
        rule['UserIdGroupPairs'] = sg_list

        return True, rule

    def delete_rule(self, groups, egress_rule, ip_protocol=None,
                    from_port=None, to_port=None,
                    ipv4_cidr=None,
                    ipv6_cidr=None,
                    security_groups=None,
                    icmp_type=None, icmp_code=None, sfunc=None):
        """Delete a Rule.

        groups can be a (comma separated) string or a collection
        of groupids, groupnames or a mix of both.
        """
        if not groups:
            return False, 'No groups specified'

        groups, err = self.ec2_sg_manager.\
            validate_and_get_security_groups(groups)
        if not groups:
            return False, err

        if not self.ignore_field(ip_protocol) and \
                ip_protocol not in self.ip_protocol_list:
            return False, f'Invalid ip_protocol : {ip_protocol}'

        if not self.ignore_field(ip_protocol) and \
                ip_protocol == 'any':
            ip_protocol = '-1'

        if not self.ignore_field(security_groups):
            security_groups, err = self.ec2_sg_manager.\
                validate_and_get_security_groups(security_groups)
            if not security_groups:
                return False, err

        aok, from_port, to_port = \
            util.validate_range(from_port, to_port)
        if not aok:
            return False, f'Invalid Network Ports : {from_port}-{to_port}'

        if not self.ignore_field(ipv4_cidr):
            ipv4_cidr, err = util.str_to_set(ipv4_cidr)
            if err:
                return False, err

        if not self.ignore_field(ipv6_cidr):
            ipv6_cidr, err = util.str_to_set(ipv6_cidr)
            if err:
                return False, err

        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            sg_dict = defaultdict(lambda: [])
            rule_match_count = 0
            for group in groups:
                for rule in self.get_rule_json(group, egress_rule):
                    aok, rule = self.\
                        match_rule(rule, ip_protocol, from_port, to_port,
                                   ipv4_cidr, ipv6_cidr, security_groups,
                                   icmp_type, icmp_code)
                    if not aok:
                        continue
                    rule_match_count += 1
                    sg_group = \
                        self.ec2_sg_manager.get_ec2_session().\
                        get_ec2_resource().\
                        SecurityGroup(group['GroupId'])
                    sg_dict[sg_group].append(rule)

            success_count = 0
            failure_count = 0
            for group, rule_list in sg_dict.items():
                _, err = self.\
                    delete_security_group_rule(group, rule_list,
                                               egress_rule,
                                               sfunc)
                if err:
                    failure_count += 1
                    sfunc(err)
                else:
                    success_count += 1

            if groups and rule_match_count == 0:
                noop_msg = 'No Rules Matched Input Criteria'
            else:
                noop_msg = 'No Instances Selected'

            return self.ec2_sg_manager.get_ec2_session().\
                get_status(success_count, failure_count,
                           noop_msg=noop_msg)
        except ClientError as client_err:
            return False, str(client_err)

    @staticmethod
    def create_security_group_rule(security_group,
                                   rule_json,
                                   egress_rule=False,
                                   sfunc=None):
        """Create a Security Group Rule."""
        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if not egress_rule:
                sfunc('Creating Ingress Rule For Group : ' +
                      f'{security_group.group_name}')
                security_group.authorize_ingress(
                    IpPermissions=rule_json)
            else:
                sfunc('Creating Egress Rule For Group : ' +
                      f'{security_group.group_name}')
                security_group.authorize_egress(
                    IpPermissions=rule_json)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)

    @staticmethod
    def delete_security_group_rule(security_group, rule_json,
                                   egress_rule, sfunc):
        """Delete a Security Group Rule."""
        def default_status(status_str):
            print(status_str)

        if not sfunc:
            sfunc = default_status

        try:
            if not egress_rule:
                sfunc('Deleting Ingress Rule For Group : ' +
                      f'{security_group.group_name}')
                security_group.revoke_ingress(
                    IpPermissions=rule_json)
            else:
                sfunc('Deleting Egress Rule For Group : ' +
                      f'{security_group.group_name}')
                security_group.revoke_egress(
                    IpPermissions=rule_json)
            return True, None
        except ClientError as client_err:
            return False, str(client_err)


if __name__ == '__main__':
    pass
