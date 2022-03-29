# Global Entry Sns Bot

Bot to monitor and alert via AWS SNS if a slot is available at a Global Entry Interview location.

Much was derived from [guoguo12/global-entry-bot](https://github.com/guoguo12/global-entry-bot)

### Find the location you are interested in
You can find the locations and their relevant codes by going to 

https://ttp.cbp.dhs.gov/schedulerapi/locations/

and selecting the matching ID for the location you want to take your interview at.

### Run
Can be run on a schedule or manually:
```commandline
python main.py -l {code} -t {topic_arn}
```

There are several configurations options that can be used when running this module.

For configuration help run:
```commandline
python main.py --help
```

### AWS Config
Ensure that the profile running is titled 'GlobalEntryBot', or modify the main to exclude a profile name.