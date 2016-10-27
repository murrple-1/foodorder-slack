from slackbot.bot import respond_to, listen_to, default_reply

@respond_to('^:todaysmenu (.*)')
def set_todays_menu(message, todays_menu_url):
    message.reply('I\'ve set today\'s menu to \'{0}\''.format(todays_menu_url))

@listen_to('^:todaysmenu$')
def todays_menu_listen(message):
    todaysMenu = _todays_menu()
    message.send(todaysMenu)

@respond_to('^:todaysmenu$')
def todays_menu_respond(message):
    todaysMenu = _todays_menu()
    message.reply(todaysMenu)

def _todays_menu():
    return 'Today\'s menu is: {0}'.format('McDonald\'s')

@respond_to('^:myorder (.*)')
def set_order(message, order):
    message.reply('Thank you for your order')

@respond_to('^:todaysorders$')
def todays_orders(message):
    message.reply('I ordered the fish')

@respond_to('^:help$')
def help(message):
    helpText = u"""
List of available commands:

\u2022 `:help` print this help message
\u2022 `:todaysmenu [MENU_URL]` set today's menu
\u2022 `:todaysmenu` get today\'s available menus
\u2022 `:myorder [YOUR_ORDER]` set your order for the day
\u2022 `:todaysorders` get list of today's orders
"""
    message.reply(helpText)

@default_reply()
def default_reply(message):
    reply = 'Sorry, but I didn\' understand you. DM me `:help` to see the complete list of commands'
    message.reply(reply)
