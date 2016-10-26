import time
import datetime
import collections
import random

from six.moves import _thread

import slackbot_settings as settings

def _run_thread(slackclient, schedule_times, channel_ids, messages):
    while True:
        now = datetime.datetime.now()
        for schedule_time in schedule_times:
            if schedule_time.dayofweek == now.weekday() and schedule_time.hour == now.hour and schedule_time.minute == now.minute:
                message = random.choice(messages)
                for channel_id in channel_ids:
                    slackclient.send_message(channel_id, message)
                break

        time.sleep(60)

def start_announce_thread(slackclient):
    willAnnounce = getattr(settings, 'ANNOUNCE_WILL_LAUNCH', False)
    if willAnnounce:
        channel_ids = []
        if isinstance(settings.ANNOUNCE_CHANNEL_NAMES, basestring):
            channel_id = slackclient.find_channel_by_name(settings.ANNOUNCE_CHANNEL_NAMES)
            if not channel_id:
                raise RuntimeError('channel id not found for \'{}\''.format(settings.ANNOUNCE_CHANNEL_NAMES))

            channel_ids.append(channel_id)
        else:
            for channelName in settings.ANNOUNCE_CHANNEL_NAMES:
                channel_id = slackclient.find_channel_by_name(channelName)
                if not channel_id:
                    raise RuntimeError('channel id not found for \'{}\''.format(channelName))

                channel_ids.append(channel_id)

        messages = []
        if isinstance(settings.ANNOUNCE_MESSAGES, basestring):
            messages.append(settings.ANNOUNCE_MESSAGES)
        else:
            messages.extend(settings.ANNOUNCE_MESSAGES)

        _thread.start_new_thread(_run_thread, (slackclient, settings.ANNOUNCE_SCHEDULE_TIMES, channel_ids, messages,))
