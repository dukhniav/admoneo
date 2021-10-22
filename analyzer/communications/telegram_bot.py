#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from typing import Dict
import time
import schedule
import requests

from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from ..logger import Logger
from ..configuration.configuration import Config
from ..communications import STATUS, utils
from ..communications import handlers
from ..configuration import constants


class TelegramBot:
    def __init__(self, logger: Logger, config: Config):
        self.logger = logger
        self.config = config
        self.logger.info("Setting up telegram comms...")
        self.enabled = utils.setup_telegram_constants(
            config, logger)
        self.token = config.TGRAM_TOKEN
        self.chat_id = config.TGRAM_CHAT_ID

        self.updater = Updater(self.config.TGRAM_TOKEN)
        self.dispatcher = self.updater.dispatcher
        self.updater.start_polling()

    def send_msg(self, msg):
        send_text = 'https://api.telegram.org/bot' + self.token + \
            '/sendMessage?chat_id=' + self.chat_id + '&parse_mode=Markdown&text=' + msg

        response = requests.get(send_text)

        return response.json()

    # def report(self):
    #     my_balance = 10   ## Replace this number with an API call to fetch your account balance
    #     my_message = "Current balance is: {}".format(my_balance)   ## Customize your message
    #     self.send_msg(my_message)
