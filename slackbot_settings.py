import os

API_TOKEN = os.environ.get('SLACKBOT_API_TOKEN') or '<your-api-token>'

ERRORS_TO = os.environ.get('SLACKBOT_ERRORS_TO') or '<your-slackbot-admin>'

PLUGINS = [
    'foodbot'
]
