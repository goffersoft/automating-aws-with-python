### notbot - cloudwatch-slack integration 

#### Send AWS CloudWatch Notifications to Slack 

#####  For This to work - the following will need to be in place.
```
1) Setup an Auto Scaling group
    a) Quick and Dirty approach
        1) create an ec2 instance
        2) add the ec2 instance to an autoscaling group
        3) add scale-up policy to the auto scaling group
               'add one instance when avg. cpu util > 50'
        4) add scale-down policy to the auto scaling group
               'remove one instance when avg. cpu util < 20'
        5) Execute the scale-up policy manually or by stressing the ec2 instance.
        6) The scale-down policy gets executed automatically.
```
