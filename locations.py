import json
import logging
import os
import sys

import requests

from configuration import LOCATIONS_API_URL, LOCATIONS_FILE_NAME


def get_location_name(location_code):
    locations = get_location_list()
    for location in locations:
        if location['id'] == int(location_code):
            return location['name']
    logging.error("Failed to match the location code {} with a location name".format(location_code))
    raise Exception("No match found for location code " + location_code)


def retrieve_locations_list():
    try:
        return requests.get(LOCATIONS_API_URL).json()
    except requests.ConnectionError:
        logging.exception('Could not connect to Locations API')
        sys.exit(1)


def save_locations_list():
    locations = retrieve_locations_list()
    with open(LOCATIONS_FILE_NAME, 'w') as file:
        json.dump(locations, file)


def load_locations_list():
    with open(LOCATIONS_FILE_NAME, 'r') as file:
        return json.load(file)


def get_location_list():
    if not os.path.exists(LOCATIONS_FILE_NAME):
        save_locations_list()
    return load_locations_list()
