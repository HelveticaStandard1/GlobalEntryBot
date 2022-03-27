import argparse
import logging
import sys
from datetime import datetime, timedelta
import boto3
import requests
from botocore.exceptions import ClientError

from configuration import *

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


def get_first_opening(location_name, location_code):
    start = datetime.now()
    end = start + timedelta(weeks=DELTA)

    url = SCHEDULER_API_URL.format(location=location_code,
                                   start=start.strftime(TTP_TIME_FORMAT),
                                   end=end.strftime(TTP_TIME_FORMAT))
    try:
        results = requests.get(url).json()  # List of flat appointment objects
    except requests.ConnectionError:
        logging.exception('Could not connect to scheduler API')
        sys.exit(1)

    for result in results:
        if result['active'] == 0:
            logging.info('Opening found for {}'.format(location_name))
            return result

    logging.info('No openings for {}'.format(location_name))


def build_message(location_name, result):
    timestamp = datetime.strptime(result['timestamp'], TTP_TIME_FORMAT)
    message = NOTIFY_MESSAGE.format(location=location_name,
                                    date=timestamp.strftime(MESSAGE_TIME_FORMAT))
    logging.info("Message Generated to be sent: {}".format(message))
    return message


def get_location_name(location_code):
    try:
        locations = requests.get(LOCATIONS_API_URL).json()
        for location in locations:
            if location['id'] == int(location_code):
                return location['name']
        logging.error("Failed to match the location code {} with a location name".format(location_code))
        raise Exception("No match found for location code " + location_code)
    except requests.ConnectionError:
        logging.exception('Could not connect to Locations API')
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='store_true', default=False)
    parser.add_argument('--location_code', '-l', help="Location code")
    parser.add_argument('--topic_arn', '-t', help="AWS Topic ARN to send valid openings to")
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format=LOGGING_FORMAT,
                            level=logging.INFO,
                            stream=sys.stdout)

    if not args.location_code:
        logging.info(
            "Cannot parse location code correctly.  Please set location code in argument ie. 'python main.py -l {"
            "location_code}")
        raise Exception("Cannot parse location code arguments")

    if not args.topic_arn:
        logging.info(
            "Cannot parse topic correctly.  Please set topic in arguments ie. 'python main.py -t {topic_arn}")
        raise Exception("Cannot parse topic arn argument")

    logging.info('Starting checks for location code: {}'.format(args.location_code))
    location_name = get_location_name(args.location_code)
    result = get_first_opening(location_name, args.location_code)
    if result:
        message = build_message(location_name, result)
        send_notification(message, args.topic_arn)
    logging.info("Main Completed")


if __name__ == '__main__':
    main()
