#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Cloud Watch alarm Manager Class."""

from types import MappingProxyType
from botocore.exceptions import ClientError


class CWAlarmManager():
    """CW Alarm Manager Class."""

    operator_map = MappingProxyType({
        'GreaterThanOrEqualToThreshold': '>=',
        'GreaterThanThreshold': '>',
        'LessThanThreshold': '<',
        'LessThanOrEqualToThreshold': '<='
    })

    def __init__(self, cw_session):
        """Initialize Cloud Watch alarm Manager Class."""
        self.cw_session = cw_session

    @staticmethod
    def print_basic_fields(alarm, rule_type_label, index):
        """Print Basic Fields Of an Alarm."""
        if index == 1:
            print()
            print(f'{rule_type_label} : ')
            print()

        print(f'{80 * "*"}')

        print(f'Namespace : {alarm.get("Namespace", "N/A")}')
        print(f'Name : {alarm["AlarmName"]}')
        print(f'Description : {alarm.get("AlarmDescription", "N/A")}')
        print(f'ARN: {alarm["AlarmArn"]}')
        print('Execute Alarm Actions : ' +
              f'{"Enabled" if alarm["ActionsEnabled"] else "Disabled"}')

    @staticmethod
    def print_alarm_action(alarm):
        """Print Alarm Actions."""
        print()
        print('AlarmActions : ')
        for action in alarm['AlarmActions']:
            print(f'{4 * " "} {action}')

    def list_metric_alarms(self, long_version=False, pfunc=None):
        """List CloudWatch metric alarms."""
        index = 1

        def print_metric_alarm_rule(alarm):
            print()
            print('AlarmRule : ')
            opname = self.operator_map.get(alarm['ComparisonOperator'],
                                           alarm['ComparisonOperator'])

            num_data_points = alarm.get('DatapointsToAlarm', 1)
            eval_periods = alarm.get('EvaluationPeriods', num_data_points)

            data_point_str = f'for {num_data_points} datapoints'
            if eval_periods != num_data_points:
                data_point_str = f'for {num_data_points} out of ' + \
                    f'{eval_periods} datapoints'

            print(f'{4 * " "}Execute Alarm Actions if ' +
                  f'{alarm["Statistic"]} {alarm["MetricName"]} ' +
                  f'{opname} {alarm["Threshold"]} ' +
                  f'{data_point_str} within a period of ' +
                  f'{alarm["Period"]} seconds')

        def default_print(alarm):
            nonlocal index

            self.print_basic_fields(alarm, 'Metric Alarms', index)
            print_metric_alarm_rule(alarm)
            self.print_alarm_action(alarm)

            if long_version:
                print()
                print(alarm)
                print()

            index += 1

        if not pfunc:
            pfunc = default_print

        try:
            for alarm in self.cw_session.get_metric_alarms():
                pfunc(alarm)
            return True, None
        except ClientError as client_error:
            return False, str(client_error)

    def list_composite_alarms(self, long_version=False, pfunc=None):
        """List CloudWatch composite alarms."""
        index = 1

        def print_composite_alarm_rules(alarm):
            print()
            print('AlarmRules : ')
            for rule in alarm["AlarmRule"].splitlines():
                print(f'{4 * " "}{rule}')

        def default_print(alarm):
            nonlocal index

            self.print_basic_fields(alarm, 'Composite Alarms', index)
            print_composite_alarm_rules(alarm)
            self.print_alarm_action(alarm)

            if long_version:
                print()
                print(alarm)
                print()

            index += 1

        if not pfunc:
            pfunc = default_print

        try:
            for alarm in self.cw_session.get_composite_alarms():
                pfunc(alarm)
            return True, None
        except ClientError as client_error:
            return False, str(client_error)


if __name__ == '__main__':
    pass
