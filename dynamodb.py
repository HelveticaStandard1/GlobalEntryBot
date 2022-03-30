import logging
from datetime import timedelta, datetime

import boto3
from botocore.exceptions import ClientError

session = boto3.session.Session(profile_name='GlobalEntryBot')
dynamodb_client = session.client('dynamodb')


def _get_time_to_live():
    return str((datetime.now() + timedelta(days=1)).timestamp()).split('.')[0]


def _create_put_item_input(location_id, timestamp):
    return {
        "TableName": "GlobalEntryTracker",
        "Item": {
            "LocationId": {"S": location_id},
            "Timestamp": {"S": timestamp},
            "TTL": {"N": _get_time_to_live()}
        }
    }


def _execute_put_item(input):
    try:
        dynamodb_client.put_item(**input)
        logging.info("Successfully put item.")
    except ClientError as error:
        logging.error("Error occurred while getting item: ", error)


def _create_get_item_input(location_id, timestamp):
    return {
        "TableName": "GlobalEntryTracker",
        "Key": {
            "LocationId": {"S": location_id},
            "Timestamp": {"S": timestamp}
        }
    }


def _execute_get_item(input):
    try:
        response = dynamodb_client.get_item(**input)
        logging.info("Successfully get item.")
        return response
    except ClientError as error:
        logging.error("Error occurred while getting item: ", error)


def get_item(location_id, timestamp):
    logging.info("Retrieving item {} - {} from Dynamodb Started".format(location_id, timestamp))
    get_item_input = _create_get_item_input(location_id, timestamp)
    response = _execute_get_item(get_item_input)
    logging.info("Retrieving item {} - {} from Dynamodb Completed".format(location_id, timestamp))
    if 'Item' in response:
        return response['Item']
    return None


def put_item(location_id, timestamp):
    logging.info("Putting item {} - {} to Dynamodb Started".format(location_id, timestamp))
    put_item_input = _create_put_item_input(location_id, timestamp)
    _execute_put_item(put_item_input)
    logging.info("Putting item {} - {} to Dynamodb Completed".format(location_id, timestamp))
