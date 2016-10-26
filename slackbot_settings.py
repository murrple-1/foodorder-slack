import os

API_TOKEN = os.environ.get('SLACKBOT_API_TOKEN') or '<your-api-token>'

ERRORS_TO = os.environ.get('SLACKBOT_ERRORS_TO') or '<your-slackbot-admin>'

PLUGINS = [
    'foodbot'
]

# Custom FoodBot settings

from scheduletime import ScheduleTime

ANNOUNCE_WILL_LAUNCH = True # bool: will the announce thread launch
ANNOUNCE_SCHEDULE_TIMES = [ScheduleTime(4, 10, 0)] # list of ScheduleTime: dayofweek/hour/minute when announcement will be made
ANNOUNCE_CHANNEL_NAMES = os.environ.get('ANNOUNCE_CHANNEL_NAME') or '<announce-channel-name>' # str, or list of str: channel name, or list of channel names, all of which receive the announcement
# ANNOUNCE_CHANNEL_NAMES = ['<announce-channel-name-1>', '<announce-channel-name-2>',]
ANNOUNCE_MESSAGES = 'Lunch Orders Please' # str, or list of str: announcement text, or list of possible texts - randomly selected during each announcement
# ANNOUNCE_MESSAGES = ['Lunch Orders Please', 'Who wants food?',]
