import re

from slackbot.bot import respond_to, listen_to, default_reply

@respond_to('today\'s menu is (.*)', re.IGNORECASE)
def set_todays_menu(message, todays_menu_url):
    message.reply('I\'ve set today\'s menu to \'{0}\''.format(todays_menu_url))

@listen_to('what\'s today\'s menu?', re.IGNORECASE)
def todays_menu_listen(message):
    todaysMenu = _todays_menu()
    message.send(todaysMenu)

@respond_to('what\'s today\'s menu?', re.IGNORECASE)
def todays_menu_respond(message):
    todaysMenu = _todays_menu()
    message.reply(todaysMenu)

def _todays_menu():
    return 'Today\'s menu is: {0}'.format('McDonald\'s')

@respond_to('my order: (.*)', re.IGNORECASE)
def set_order(message, order):
    message.reply('Thank you for your order')

@respond_to('what are today\'s orders?')
def todays_orders(message):
    message.reply('I ordered the fish')

@default_reply()
def default_reply(message):
    reply = u'Sorry, but I didn\' understand you'
    message.reply(reply)
