import logging

import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session(profile_name='GlobalEntryBot')
sns = session.client('sns')


def send_notification(message, topic_arn, subject):
    logging.info("Posting message '{}' to topic ARN {}".format(message, topic_arn))
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        logging.info("Published Message ID: {}".format(response['MessageId']))
    except ClientError as ex:
        logging.exception("Client Error occurred when attempting to send to SNS.", '', ex)
        raise ex
