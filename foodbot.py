import re

from slackbot.bot import respond_to, listen_to, default_reply

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')

@respond_to('I love you')
def love(message):
    message.reply('I love you too!')

@listen_to('Can someone help me?')
def help(message):
    # Message is replied to the sender (prefixed with @user)
    # message.reply('Yes, I can!')

    # Message is sent on the channel
    message.send('I can help everybody!')

@default_reply
def default_reply(message):
    reply = u'Sorry, but I didn\' understand you\nAvailable commands:\n{0}'.format(message.docs_reply())
    message.reply(reply)
