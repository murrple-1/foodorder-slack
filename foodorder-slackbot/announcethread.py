import time
import datetime
import random
import threading

import slackbot_settings as settings

import slacker

from log import logger
from cron import CronScheduleTime, parse_cron_schedule


def _run_thread(slackclient, cron_schedule_times, channel_ids, messages):
    while True:
        now = datetime.datetime.now()
        logger().info('checking announce thread')

        for cron_schedule_time in cron_schedule_times:
            logger().debug('checking cron-time: %s', cron_schedule_time)

            if cron_schedule_time.is_on(now):

                message = random.choice(messages)

                logger().info('schedule time found, sending message: \'%s\'', message)

                for channel_id in channel_ids:
                    try:
                        slackclient.send_message(channel_id, message)
                    except slacker.Error as e:
                        logger().error('Error sending Slack message to channel \'%s\': %s', channel_id, e)
                break

        time.sleep(60)


def start_announce_thread(slackclient):
    will_announce = getattr(settings, 'ANNOUNCE_WILL_LAUNCH', False)
    if will_announce:
        channel_ids = []
        if isinstance(settings.ANNOUNCE_CHANNEL_NAMES, str):
            channel_id = slackclient.find_channel_by_name(
                settings.ANNOUNCE_CHANNEL_NAMES)
            if not channel_id:
                raise RuntimeError(
                    'channel id not found for \'{}\''.format(
                        settings.ANNOUNCE_CHANNEL_NAMES))

            channel_ids.append(channel_id)
        else:
            for channelName in settings.ANNOUNCE_CHANNEL_NAMES:
                channel_id = slackclient.find_channel_by_name(channelName)
                if not channel_id:
                    raise RuntimeError(
                        'channel id not found for \'{}\''.format(channelName))

                channel_ids.append(channel_id)

        messages = []
        if isinstance(settings.ANNOUNCE_MESSAGES, str):
            messages.append(settings.ANNOUNCE_MESSAGES)
        else:
            messages.extend(settings.ANNOUNCE_MESSAGES)

        cron_schedule_times = []
        for cron_schedule_time in settings.ANNOUNCE_CRON_SCHEDULE_TIMES:
            if isinstance(cron_schedule_time, CronScheduleTime):
                cron_schedule_times.append(cron_schedule_time)
            else:
                cron_schedule_times.append(
                    parse_cron_schedule(cron_schedule_time))

        thread = threading.Thread(
            target=_run_thread,
            args=(
                slackclient,
                cron_schedule_times,
                channel_ids,
                messages,
            ),
            daemon=True)
        thread.start()
