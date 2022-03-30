import json
import logging
import os
import sys

import requests

from configuration import LOCATIONS_API_URL, LOCATIONS_FILE_NAME

dirname = os.path.dirname(os.path.abspath(__file__))
locations_file_path = os.path.join(dirname, LOCATIONS_FILE_NAME)

def get_location_name(location_code):
    locations = get_location_list()
    for location in locations:
        if location['id'] == int(location_code):
            return location['name']
    logging.error("Failed to match the location code {} with a location name".format(location_code))
    raise Exception("No match found for location code " + location_code)


def retrieve_locations_list():
    try:
        logging.info("Retrieving Locations List from repository")
        response = requests.get(LOCATIONS_API_URL).json()
        logging.info("Locations list retrieved successfully")
        return response
    except requests.ConnectionError:
        logging.exception('Could not connect to Locations API')
        sys.exit(1)


def save_locations_list():
    locations = retrieve_locations_list()
    logging.info("Saving locations list to working directory")
    with open(locations_file_path, 'w') as file:
        json.dump(locations, file)
    logging.info("Saved without error")


def load_locations_list():
    with open(locations_file_path, 'r') as file:
        return json.load(file)


def get_location_list():
    if not os.path.exists(locations_file_path):
        logging.info("Locations list is not present in the working directory")
        save_locations_list()
    return load_locations_list()
