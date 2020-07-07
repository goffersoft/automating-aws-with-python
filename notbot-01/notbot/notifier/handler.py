import os
import requests

def post_to_slack(event, context):
    """
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
    """

    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    slack_message = 'From {source} at ' + \
                    '{detail[StartTime]}: {detail[Description]}'
    slack_message = slack_message.format(**event)

    data = { "text": slack_message }
    requests.post(slack_webhook_url, json=data)

    print(slack_webhook_url)
    print(event)

    return
