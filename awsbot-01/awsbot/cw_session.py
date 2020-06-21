#! /usr/bin/python
# -*- coding:utf-8 -*-

"""Cloud Watch Session Manager Class."""


class CWSessionManager():
    """CloudWatch Session Manager Class."""

    def __init__(self, session):
        """Initialize the CloudWatch Session Manager class."""
        self.session = session

    def get_cw_client(self):
        """Get cloud watch client."""
        return self.session.get_client('cloudwatch')

    def get_cw_paginator(self, name):
        """Get cloudwatch paginator."""
        try:
            return self.get_cw_client().get_paginator(name), None
        except KeyError as key_error:
            return None, str(key_error)

    def get_describe_alarms_paginator(self):
        """Get cloudwatch 'DescribeAlarms' paginator."""
        return self.get_cw_paginator('describe_alarms')[0]

    def get_alarms(self, alarm_type_config, alarm_type_label):
        """Iterate over cloud watch alarms."""
        paginator = self.get_describe_alarms_paginator()

        for page in paginator.paginate(AlarmTypes=[alarm_type_config]):
            for alarm in page[alarm_type_label]:
                yield alarm

    def get_metric_alarms(self):
        """Iterate over cloud watch metric alarms."""
        return self.get_alarms('MetricAlarm', 'MetricAlarms')

    def get_composite_alarms(self):
        """Iterate over cloud watch composite alarms."""
        return self.get_alarms('CompositeAlarm', 'CompositeAlarms')


if __name__ == '__main__':
    pass
