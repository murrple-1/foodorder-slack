from slackbot.bot import respond_to, listen_to, default_reply

import sqlite3
import datetime
import calendar
import re

from log import logger

def _dayInterval(date=None):
    if date is None:
        date = datetime.date.today()

    start = datetime.datetime(date.year, date.month, date.day, 0, 0, 0, 0)
    end = datetime.datetime(date.year, date.month, date.day, 23, 59, 59, 999999)
    return start, end

_MENU_NAME_REGEX = r'[^\f\r\n\v\']+'
_MENU_URL_REGEX = (
    # protocol identifier
    r'(?:https?:/)'
    # host name
    r'(?:(?:[a-z0-9]-?)*[a-z0-9]+)'
    # domain name
    r'(?:\.(?:[a-z0-9]-?)*[a-z0-9]+)*'
    # TLD identifier
    r'(?:\.(?:[a-z]{2,}))'
    # port number
    r'(?::\d{2,5})?'
    # resource path
    r'(?:/\s*)?'
)
_MY_ORDER_REGEX = r'[^\f\r\n\v\']+'

def _slack_regex_group(regex):
    return '({0})'.format(regex)

def _slack_url_regex_group(url_regex):
    return '<({0})>'.format(url_regex)

def _remove_old_entries(cur, dayStart):
    cur.execute(
        """
        DELETE FROM \"daily_menus\"
        WHERE `date` < :day_start
        """, { 'day_start': calendar.timegm(dayStart.utctimetuple()) }
    )

    cur.execute(
        """
        DELETE FROM \"orders\"
        WHERE `ordered_at` < :day_start
        """, { 'day_start': calendar.timegm(dayStart.utctimetuple()) }
    )

@respond_to('^:addtodaysmenu \'{0}\' \'{1}\'$'.format(_slack_regex_group(_MENU_NAME_REGEX), _slack_url_regex_group(_MENU_URL_REGEX)))
def add_today_menu(message, menu_name, menu_url):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        exists = cur.execute(
            """
            SELECT dlm.`id` FROM \"daily_menus\" AS dlm
            WHERE dlm.`name` = :menu_name AND (dlm.`date` >= :day_start AND dlm.`date` <= :day_end)
            LIMIT 1
            """, { 'menu_name': menu_name, 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()) }
        ).fetchone()

        if exists:
            cur.execute(
                """
                UPDATE \"daily_menus\"
                SET `url` = :url
                WHERE `id` = :id
                """, { 'url': menu_url, 'id': exists[0] }
            )

            conn.commit()

            message.reply('Updated today\'s menu')
        else:
            cur.execute(
                """
                INSERT INTO \"daily_menus\" (`name`, `url`, `date`) VALUES
                (:name, :url, :date)
                """, { 'name': menu_name, 'url': menu_url, 'date': calendar.timegm(datetime.datetime.now().utctimetuple()) }
            )

            conn.commit()

            message.reply('Added \'{0}\' to today\'s menu'.format(menu_name))
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:removetodaysmenu \'{0}\'$'.format(_slack_regex_group(_MENU_NAME_REGEX)))
def remove_today_menu(message, menu_name):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        exists = cur.execute(
            """
            SELECT dlm.`id` FROM \"daily_menus\" AS dlm
            WHERE dlm.`name` = :menu_name AND (dlm.`date` >= :day_start AND dlm.`date` <= :day_end)
            LIMIT 1
            """, { 'menu_name': menu_name, 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()) }
        ).fetchone()

        if exists:
            cur.execute(
                """
                DELETE FROM \"daily_menus\"
                WHERE `id` = :id
                """, { 'id': exists[0] }
            )

            conn.commit()

            message.reply('Removed menu item')
        else:
            message.reply('No menu item found, so nothing removed')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:adddefaultmenu \'{0}\' \'{1}\'$'.format(_slack_regex_group(_MENU_NAME_REGEX), _slack_url_regex_group(_MENU_URL_REGEX)))
def add_default_menu(message, menu_name, menu_url):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        exists = cur.execute(
            """
            SELECT dfm.`id` FROM \"default_menus\" AS dfm
            WHERE dfm.`name` = :menu_name
            LIMIT 1
            """, { 'menu_name': menu_name }
        ).fetchone()

        if exists:
            cur.execute(
                """
                UPDATE \"default_menus\"
                SET `url` = :url
                WHERE `id` = :id
                """, { 'url': menu_url, 'id': exists[0] }
            )

            conn.commit()

            message.reply('Updated default menu')
        else:
            cur.execute(
                """
                INSERT INTO \"default_menus\" (`name`, `url`) VALUES
                (:name, :url)
                """, { 'name': menu_name, 'url': menu_url}
            )

            conn.commit()

            message.reply('Added \'{0}\' to default menu'.format(menu_name))
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:removedefaultmenu \'{0}\'$'.format(_slack_regex_group(_MENU_NAME_REGEX)))
def remove_default_menu(message, menu_name):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        exists = cur.execute(
            """
            SELECT dfm.`id` FROM \"daily_menus\" AS dfm
            WHERE dfm.`name` = :menu_name
            LIMIT 1
            """, { 'menu_name': menu_name }
        ).fetchone()

        if exists:
            cur.execute(
                """
                DELETE FROM \"default_menus\"
                WHERE `id` = :id
                """, { 'id': exists[0] }
            )

            conn.commit()

            message.reply('Removed default menu item')
        else:
            message.reply('No default menu item found, so nothing removed')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:resettodaysmenu$')
def reset_todays_menu(message):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        cur.execute(
            """
            DELETE FROM \"daily_menus\"
            WHERE dlm.`date` >= :day_start AND dlm.`date` <= :day_end
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()) }
        )

        conn.commit()

        message.reply('Today\'s menu has been reset')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:todaysmenu$')
def todays_menu_respond(message):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        menus = None

        menus = cur.execute(
            """
            SELECT dlm.`name`, dlm.`url` FROM \"daily_menus\" AS dlm
            WHERE dlm.`date` >= :day_start AND dlm.`date` <= :day_end
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()) }
        ).fetchall()

        if len(menus) < 1:
            menus = cur.execute(
                """
                SELECT dfm.`name`, dfm.`url` FROM \"default_menus\" AS dfm
                """
            ).fetchall()

        if len(menus) > 0:
            replyLines = []
            for menu in menus:
                replyLines.append(u'\u2022 {0} - {1}'.format(menu[0], menu[1]))

            reply = u'\n'.join(replyLines)

            message.reply(reply)
        else:
            message.reply('No menu has been set')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:myorder$')
def echo_order(message):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        oldOrder = cur.execute(
            """
            SELECT o.`text` FROM \"orders\" AS o
            WHERE (o.`ordered_at` >= :day_start AND o.`ordered_at` <= :day_end) AND o.`ordered_by` = :ordered_by
            LIMIT 1
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()), 'ordered_by': message.body['user'] }
        ).fetchone()

        if oldOrder:
            conn.commit()

            message.reply('You ordered: \'{0}\''.format(oldOrder[0]))
        else:
            conn.commit()

            message.reply('You haven\'t made an order yet today')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:myorder \'{0}\''.format(_slack_regex_group(_MY_ORDER_REGEX)))
def set_order(message, order):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        oldOrder = cur.execute(
            """
            SELECT o.`id` FROM \"orders\" AS o
            WHERE (o.`ordered_at` >= :day_start AND o.`ordered_at` <= :day_end) AND o.`ordered_by` = :ordered_by
            LIMIT 1
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()), 'ordered_by': message.body['user'] }
        ).fetchone()

        if oldOrder:
            cur.execute(
                """
                UPDATE \"orders\"
                SET `text` = :text
                WHERE `id` = :id
                """, { 'text': order, 'id': oldOrder[0] }
            )

            conn.commit()

            message.reply('Order updated')
        else:
            cur.execute(
                """
                INSERT INTO \"orders\" (`ordered_at`, `ordered_by`, `text`) VALUES
                (:ordered_at, :ordered_by, :text)
                """, { 'ordered_at': calendar.timegm(datetime.datetime.now().utctimetuple()), 'ordered_by': message.body['user'], 'text': order }
            )

            conn.commit()

            message.reply('Added order')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:clearmyorder$')
def clear_order(message):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        _remove_old_entries(cur, dayStart)

        oldOrder = cur.execute(
            """
            SELECT o.`id` FROM \"orders\" AS o
            WHERE (o.`ordered_at` >= :day_start AND o.`ordered_at` <= :day_end) AND o.`ordered_by` = :ordered_by
            LIMIT 1
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()), 'ordered_by': message.body['user'] }
        ).fetchone()

        if oldOrder:
            cur.execute(
                """
                DELETE FROM \"orders\"
                WHERE `id` = :id
                """, { 'id': oldOrder[0] }
            )

            conn.commit()

            message.reply('Today\'s order cleared')
        else:
            message.reply('No order yet today, nothing removed')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:todaysorders$')
def todays_orders(message):
    dayStart, dayEnd = _dayInterval()
    conn = sqlite3.connect('data.db')

    try:
        cur = conn.cursor()

        todaysOrders = cur.execute(
            """
            SELECT o.`ordered_by`, o.`text`
            FROM \"orders\" AS o
            WHERE (o.`ordered_at` >= :day_start AND o.`ordered_at` <= :day_end)
            """, { 'day_start': calendar.timegm(dayStart.utctimetuple()), 'day_end': calendar.timegm(dayEnd.utctimetuple()) }
        ).fetchall()

        def _userid_to_username(userid, slackclient):
            from six import iteritems

            for _userid, user in iteritems(slackclient.users):
                if userid == _userid:
                    return user['name']

        if len(todaysOrders) > 0:
            replyLines = []
            for todaysOrder in todaysOrders:
                username = _userid_to_username(todaysOrder[0], message._client)
                replyLines.append(u'\u2022 @{0} - {1}'.format(username, todaysOrder[1]))

            reply = u'\n'.join(replyLines)

            message.reply(reply)
        else:
            message.reply('No orders put in yet today')
    finally:
        if conn is not None:
            conn.close()

@respond_to('^:help$')
def help(message):
    helpText = u"""
List of available commands:

\u2022 `:help` print this help message
\u2022 `:todaysmenu` get today's menu
\u2022 `:todaysorders` get today\'s orders
\u2022 `:myorder '[YOUR ORDER]'` set your order for the day
\u2022 `:myorder` echo your order back to you
\u2022 `:clearmyorder` unset your order for the day
\u2022 `:addtodaysmenu '[MENU NAME]' '[MENU URL]'` add a menu to today's menu
\u2022 `:removetodaysmenu '[MENU NAME]'` remove a menu from today's menu
\u2022 `:resettodaysmenu` clear today's custom menu, returning to the default state
\u2022 `:adddefaultmenu '[MENU NAME]' '[MENU URL]'` add a menu to the default menu
\u2022 `:removedefaultmenu '[MENU NAME]'` remove a menu from the default menu
"""
    message.reply(helpText)

@default_reply()
def default_reply(message):
    reply = 'Sorry, but I didn\' understand you. DM me `:help` to see the complete list of commands'
    message.reply(reply)
