#! /usr/bin/python
# -*- coding:utf-8 -*-

"""EC2 Instance Related CLI commands."""

import click

try:
    from awsbot.cli_context import cli_context
    from awsbot.ec2_instance import EC2InstanceManager
    from awsbot.ec2_session import EC2SessionManager
except ImportError:
    from cli_context import cli_context
    from ec2_instance import EC2InstanceManager
    from ec2_session import EC2SessionManager


def cli_ec2_instance_init():
    """Initialize awsbot cli for ec2 instances."""
    pass


@click.group('instance')
@cli_context
def cli_ec2_instance(session=None):
    """- AWS EC2 instances Automation Commands."""
    if not session.get_ec2_session():
        session.set_ec2_session(EC2SessionManager(session))


@cli_ec2_instance.command('list')
@click.option('--instances', default=None,
              help='list the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='list all instances for '
                   'project tag:Project:<name>')
@click.option('--states', default=None,
              help='interesting instance states to '
                   'include or exclude')
@click.option('--include-states/--exclude-states', default=None,
              help='instance states to include or '
                   'exclude in the listing')
@cli_context
def list_instances(session, instances, project_name,
                   states, include_states):
    """List EC2 instances."""
    aok, err = EC2InstanceManager(session.get_ec2_session()).\
        list_instances(instances, project_name, states, include_states)

    if not aok:
        print(err)


@cli_ec2_instance.command('start')
@click.option('--instances', default=None,
              help='start the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='start all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='start all instances for project tag:Project:<name>')
@cli_context
def start_instances(session, instances, force, project_name):
    """Start EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        start_instances(instances, project_name)

    print()
    print(err)


@cli_ec2_instance.command('stop')
@click.option('--instances', default=None,
              help='stop the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='stop all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='stop all instances for project tag:Project:<name>')
@cli_context
def stop_instances(session, instances, force, project_name):
    """Stop EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        stop_instances(instances, project_name)

    print()
    print(err)


@cli_ec2_instance.command('reboot')
@click.option('--instances', default=None,
              help='reboot the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--force', is_flag=True,
              help='reboot all ec2 instances for all projects')
@click.option('--project-name', default=None,
              help='reboot all instances for project tag:Project:<name>')
@cli_context
def reboot_instances(session, instances, force, project_name):
    """Reboot EC2 instances."""
    if not force and project_name is None:
        print('Please Specify Project Name associated with Instances')
        return

    _, err = EC2InstanceManager(session.get_ec2_session()).\
        reboot_instances(instances, project_name)

    print()
    print(err)


@cli_ec2_instance.command('create')
@click.argument('image-name')
@click.argument('instance-type')
@click.argument('security-groups')
@click.argument('key-name')
@click.option('--min-count', type=click.INT, default=1,
              help='minimum number of instances to create')
@click.option('--max-count', type=click.INT, default=1,
              help='maximum number of instances to create')
@click.option('--subnet-id', default=None,
              help='vpc to launch instance into')
@click.option('--user-data', is_flag=True,
              help='use the specified script to initialize instance')
@click.option('--user-data-file',
              default='resources/templates/script/www_script.sh',
              help='script to run after launching instance')
@click.option('--project-name', default=None,
              help='create all instances with tag:Project:<name>')
@click.option('--instance-name', default=None,
              help='name of the instance')
@click.option('--iam-instance-profile-arn', default=None,
              help='iam instance profile arn')
@cli_context
def create_instances(session, image_name, instance_type,
                     security_groups, key_name, min_count,
                     max_count, subnet_id, user_data,
                     user_data_file, project_name, instance_name,
                     iam_instance_profile_arn):
    """Create one or more EC2 instances.

    image-name - name of the image.
    instance-type - type of the instance.
    key-name - a valid key-name to login to the ec2 isntances.
    Note : image-names are the same across regions bu the
           images ids differ from region to region.
    """
    _, status = EC2InstanceManager(session.get_ec2_session()).\
        create_instances(image_name, instance_type, security_groups,
                         key_name, min_count, max_count, subnet_id,
                         user_data, user_data_file,
                         project_name, instance_name,
                         iam_instance_profile_arn)

    print()
    print(status)


@cli_ec2_instance.command('terminate')
@click.option('--instances', default=None,
              help='terminate the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--project-name', default=None,
              help='delete all instances with tag:Project:<name>')
@cli_context
def terminate_instances(session, instances, project_name):
    """Delete one or more or all EC2 instances."""
    _, status = EC2InstanceManager(session.get_ec2_session()).\
        terminate_instances(instances, project_name)

    print()
    print(status)


@cli_ec2_instance.command('modify')
@click.option('--instances', default=None,
              help='modify the selected instances '
                   '(instance-ids separated by commas)')
@click.option('--security-groups', default=None,
              help='change the security groups associated with '
                   'the instances')
@click.option('--enable-source-dest-check/--disable-source-dest-check',
              is_flag=True, default=None,
              help='enable or disable source destination check')
@click.option('--user-data', is_flag=True,
              help='modify the script to initialize instance')
@click.option('--user-data-file',
              default='resources/templates/script/www_script.sh',
              help='new script to run after launching instance')
@click.option('--project-name', default=None,
              help='modify all instances for project tag:Project:<name>')
@click.option('--instance-names', default=None,
              help='modify the selected instances '
                   '(instance-names separated by commas)')
@click.option('--iam-instance-profile-arn', default=None,
              help='iam instance profile arn to attach')
@click.option('--attach-iam-role/--detach-iam-role', default=None,
              help='attach new iam role or detach the existing iam role')
@cli_context
def modify_instances(session, instances, security_groups,
                     enable_source_dest_check, user_data,
                     user_data_file, project_name,
                     instance_names, iam_instance_profile_arn,
                     attach_iam_role):
    """Modify EC2 instances."""
    _, err = EC2InstanceManager(session.get_ec2_session()).\
        modify_instances(instances, security_groups,
                         enable_source_dest_check,
                         user_data, user_data_file,
                         project_name, instance_names,
                         iam_instance_profile_arn, attach_iam_role)

    print()
    print(err)


if __name__ == '__main__':
    cli_ec2_instance_init()
    cli_ec2_instance()
