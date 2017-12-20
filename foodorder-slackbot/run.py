from slackbot.bot import Bot

import announcethread

def main():
    bot = Bot()

    announcethread.start_announce_thread(bot._client)

    bot.run()

if __name__ == '__main__':
    main()
