#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Security Group Rules Automation CLI Commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot import util
    from awsbot.ec2_security_group import EC2SecurityGroupManager
    from awsbot.ec2_security_group_rule import EC2SecurityGroupRuleManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    import util
    from ec2_security_group import EC2SecurityGroupManager
    from ec2_security_group_rule import EC2SecurityGroupRuleManager
    from ec2_session import EC2SessionManager


def cli_ec2_security_group_rule_init():
    """Initialize awsbot cli for ec2 security group rules."""
    pass


@click.group('rule')
@cli_context
def cli_ec2_security_group_rule(session=None):
    """- AWS EC2 Security Group Rules Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_security_group_rule.command('create')
@click.argument('groups')
@click.option('--egress-rule', is_flag=True,
              help='indicates the rule is an egress rulw. ' +
              'Otherwise ingress rule is assumed.')
@click.option('--ip-protocol', default='any',
              help='ip protocol(tcp , udp , icmp , icmpv6, any) ' +
              'to allow. Use "any" to specify all ports')
@click.option('--port-range', default='any',
              help='port ranges(or a single port) to allow. ' +
              'Port ranges specified as <fromPort>-<toPort>.' +
              'Use "any" to specify all ports')
@click.option('--ipv4-cidr', default=None,
              help='ipv4 address(comma separated cidr blocks) to allow')
@click.option('--ipv4-descriptions', default=None,
              help='descriptions(comma separated) associated with ' +
              'ipv4 cidr blocks')
@click.option('--ipv6-cidr', default=None,
              help='ipv4 address(comma separated cidr blocks) to allow')
@click.option('--ipv6-descriptions', default=None,
              help='descriptions(comma separated) associated with ' +
              'ipv6 cidr blocks')
@click.option('--security-groups', default=None,
              help='security-groups(comma separated) to allow. ' +
              'If this is defined, then ip (v4/v6) cidr blocks ' +
              'are ignored. The input can be  a list of names ' +
              'or ids or a mix of both')
@click.option('--security-group-descriptions', default=None,
              help='descriptions(comma separated) associated with ' +
              'security groups')
@click.option('--icmp-type', default='any',
              help='applicable if protocol is icmp or icmpv6. ' +
              'specify the icmp type to allow')
@click.option('--icmp-code', default='any',
              help='applicable if protocol is icmp or icmpv6. ' +
              'specify the icmp code to allow')
@cli_context
def create_rule(session, groups, egress_rule,
                ip_protocol, port_range,
                ipv4_cidr, ipv4_descriptions,
                ipv6_cidr, ipv6_descriptions,
                security_groups, security_group_descriptions,
                icmp_type, icmp_code):
    """Create Security Group Rules."""
    aok, from_port, to_port = util.str_range_to_int(port_range)

    if not aok:
        print(f'Invalid port range : {port_range}')
        return

    aok, status = EC2SecurityGroupRuleManager(
        EC2SecurityGroupManager(session.get_ec2_session())). \
        create_rule(groups, egress_rule,
                    ip_protocol, from_port,
                    to_port, ipv4_cidr, ipv4_descriptions,
                    ipv6_cidr, ipv6_descriptions,
                    security_groups, security_group_descriptions,
                    icmp_type, icmp_code)

    print()
    print(status)


@cli_ec2_security_group_rule.command('delete')
@click.argument('groups')
@click.option('--egress-rule', is_flag=True,
              help='indicates the rule is an egress rulw. ' +
              'Otherwise ingress rule is assumed.')
@click.option('--ip-protocol', default='ignore',
              help='ip protocol(tcp , udp , icmp , icmpv6, any) ' +
              'to allow. Use "any" to specify all ports')
@click.option('--port-range', default='ignore',
              help='port ranges(or a single port) to allow. ' +
              'Port ranges specified as <fromPort>-<toPort>.' +
              'Use "any" to specify all ports')
@click.option('--ipv4-cidr', default='ignore',
              help='ipv4 address(comma separated cidr blocks) to allow')
@click.option('--ipv6-cidr', default='ignore',
              help='ipv4 address(comma separated cidr blocks) to allow')
@click.option('--security-groups', default='ignore',
              help='security-groups(comma separated) to allow. ' +
              'If this is defined, then ip (v4/v6) cidr blocks ' +
              'are ignored. The input can be  a list of names ' +
              'or ids or a mix of both')
@click.option('--icmp-type', default='ignore',
              help='applicable if protocol is icmp or icmpv6. ' +
              'specify the icmp type to allow')
@click.option('--icmp-code', default='ignore',
              help='applicable if protocol is icmp or icmpv6. ' +
              'specify the icmp code to allow')
@cli_context
def delete_rule(session, groups, egress_rule,
                ip_protocol, port_range,
                ipv4_cidr, ipv6_cidr,
                security_groups, icmp_type, icmp_code):
    """Delete Security Group Rules.

    Delete rules associated with (comma separated)
    groups. Can be group ids or group names of a mix of both'.

    Rules are selected for deletion based on a match of all
    of the above mentioned criteria.
    """
    from_port = None
    to_port = None
    wildcard = ('ignore', 'any')
    if port_range and port_range not in wildcard:
        parts = port_range.split(',')
        if parts[0] not in wildcard:
            from_port = parts[0]

        if len(parts) >= 2 and parts[1] not in wildcard:
            to_port = parts[1]

    _, status = EC2SecurityGroupRuleManager(
        EC2SecurityGroupManager(session.get_ec2_session())). \
        delete_rule(groups, egress_rule,
                    ip_protocol, from_port,
                    to_port, ipv4_cidr,
                    ipv6_cidr, security_groups,
                    icmp_type, icmp_code)

    print()
    print(status)


if __name__ == '__main__':
    cli_ec2_security_group_rule_init()
    cli_ec2_security_group_rule()
