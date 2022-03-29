SCHEDULER_API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/locations/{location}/slots?startTimestamp={start}&endTimestamp={end}'
LOCATIONS_API_URL = 'https://ttp.cbp.dhs.gov/schedulerapi/locations/'
TTP_TIME_FORMAT = '%Y-%m-%dT%H:%M'

NOTIF_MESSAGE = 'New appointment slot open at {location}: {date}'
MESSAGE_TIME_FORMAT = '%A, %B %d, %Y at %I:%M %p'
LOGGING_FORMAT = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
DEFAULT_DELTA = 10
NOTIFY_MESSAGE = 'New appointment slot open at {location}: {date}\n\nLogin to https://ttp.dhs.gov/ to schedule.'
GLOBAL_ENTRY_NOTIFICATION_SUBJECT = 'Global Entry Appointment Available'
LOCATIONS_FILE_NAME = 'locations_list.json'
