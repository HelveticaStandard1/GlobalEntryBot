import argparse
import logging
import sys
from datetime import datetime, timedelta
import boto3
import requests
from botocore.exceptions import ClientError

from configuration import *
from locations import get_location_name
from validate import validate_args

session = boto3.session.Session(profile_name='GlobalEntryBot')
sns = session.client('sns')


def send_notification(message, topic_arn):
    logging.info("Posting message '{}' to topic ARN {}".format(message, topic_arn))
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=GLOBAL_ENTRY_NOTIFICATION_SUBJECT
        )
        logging.info("Published Message ID: {}".format(response['MessageId']))
    except ClientError as ex:
        logging.exception("Client Error occurred when attempting to send to SNS.", '', ex)
        raise ex


def get_end_date(start, kwargs):
    if kwargs['end_date']:
        end = datetime.strptime(kwargs['end_date'], '%m-%d-%Y')
    elif kwargs['weeks']:
        end = start + timedelta(weeks=int(kwargs['weeks']))
    else:
        end = start + timedelta(weeks=DEFAULT_DELTA)
    return end


def get_start_and_end(kwargs):
    start = get_start_date(kwargs)
    end = get_end_date(start, kwargs)
    return start, end


def get_start_date(kwargs):
    if kwargs['start_date']:
        start = datetime.strptime(kwargs['start_date'], '%m-%d-%Y')
    else:
        start = datetime.now()
    return start


def get_first_opening(location_name, **kwargs):
    start, end = get_start_and_end(kwargs)

    url = SCHEDULER_API_URL.format(location=kwargs['location_code'],
                                   start=start.strftime(TTP_TIME_FORMAT),
                                   end=end.strftime(TTP_TIME_FORMAT))
    try:
        results = requests.get(url).json()  # List of flat appointment objects
    except requests.ConnectionError:
        logging.exception('Could not connect to scheduler API')
        sys.exit(1)

    for result in results:
        if result['active'] > 0:
            logging.info('Opening found for {}'.format(location_name))
            return result

    logging.info('No openings for {}'.format(location_name))


def build_message(location_name, result):
    timestamp = datetime.strptime(result['timestamp'], TTP_TIME_FORMAT)
    message = NOTIFY_MESSAGE.format(location=location_name,
                                    date=timestamp.strftime(MESSAGE_TIME_FORMAT))
    logging.info("Message Generated to be sent: {}".format(message))
    return message


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('--location_code', '-l', help="Location code")
    parser.add_argument('--topic_arn', '-t', help="AWS Topic ARN to send valid openings to")
    parser.add_argument('--start_date', '-s', help="Earliest Date for appointment in MM-DD-YYYY")
    parser.add_argument('--end_date', '-e', help="Latest Date for appointment in MM-DD-YYYY")
    parser.add_argument('--weeks', '-w',
                        help="Weeks from today to look for appointments.  Do not set start or end date if using weeks.")
    args = parser.parse_args()
    validate_args(args)
    logging.info('Starting checks for location code: {}'.format(args.location_code))
    location_name = get_location_name(args.location_code)
    result = get_first_opening(location_name, **vars(args))
    if result:
        message = build_message(location_name, result)
        send_notification(message, args.topic_arn)
    logging.info("Main Completed")


if __name__ == '__main__':
    main()
