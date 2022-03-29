import logging
import sys
from datetime import datetime

from configuration import LOGGING_FORMAT


def validate_args(args):
    if args.verbose:
        logging.basicConfig(format=LOGGING_FORMAT,
                            level=logging.INFO,
                            stream=sys.stdout)
    if args.weeks:
        if args.start_date or args.end_date:
            logging.error(
                "Weeks were requested with a start or end date parameter.  Can only have weeks if no start or end date is selected.")
            raise Exception("Weeks entered with start or end date parameters")

    if args.start_date and not args.end_date:
        logging.error("A start date was entered without an end date.  If one is entered the other must be.")
        raise Exception("Only start_date inputted")

    if args.end_date and not args.start_date:
        logging.error("A end date was entered without an start date.  If one is entered the other must be.")
        raise Exception("Only end_date inputted")

    if args.end_date:
        try:
            datetime.strptime(args.end_date, '%m-%d-%Y')
        except ValueError as err:
            logging.error('end_date {} does not match expected format of MM-DD-YYYY'.format(args.end_date))
            raise Exception('Incorrect end_date format')

    if args.start_date:
        try:
            start = datetime.strptime(args.start_date, '%m-%d-%Y')
            if start < datetime.now():
                logging.error('start_date {} has a midnight start before the current date/time'.format(args.start_date))
                raise Exception("Start date entered is before current date.")
        except ValueError as err:
            logging.error('start_date {} does not match expected format of MM-DD-YYYY'.format(args.start_date))
            raise Exception('Incorrect start_date format')

    if args.start_date and args.end_date:
        start_date = datetime.strptime(args.start_date, '%m-%d-%Y')
        end_date = datetime.strptime(args.end_date, '%m-%d-%Y')
        if start_date > end_date:
            logging.error("start_date {} is after end_date {}.  Dates need to be continual".format(args.start_date,
                                                                                                   args.end_date))
            raise Exception("start_date is after end_date")

    if not args.location_code:
        logging.error(
            "Cannot parse location code correctly.  Please set location code in argument ie. 'python main.py -l {"
            "location_code}")
        raise Exception("Cannot parse location code arguments")

    if not args.topic_arn:
        logging.error(
            "Cannot parse topic correctly.  Please set topic in arguments ie. 'python main.py -t {topic_arn}")
        raise Exception("Cannot parse topic arn argument")
