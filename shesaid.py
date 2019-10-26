#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import sys

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

mode = os.getenv("MODE")
token = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "pro":
    def run(updater):
        port = int(os.environ.get("PORT", "8443"))
        heroku_app_name = os.environ.get("HEROKU_APP_NAME")

        updater.start_webhook(listen="0.0.0.0",
                              port=port,
                              url_path=token)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(heroku_app_name, token))
else:
    logger.error("No MODE specified!")
    sys.exit(1)



def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text('Hi!')


def shesaid(update, context):
    triggers = ['grande', 'gorda', 'larga']
    if [ele for ele in triggers if(ele in update.message.text)]:
        update.message.reply_text("That's what she said")


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    logger.info("Starting bot")

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, shesaid))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    run(updater)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    # updater.idle()


if __name__ == '__main__':
    main()
