"""
Analzer is the main module of this bot. 
"""

import time
import logging

from analyzer import __version__, __logger__
from analyzer.loader import Loader
from analyzer.processor import Processor
from pycoingecko import CoinGeckoAPI
from analyzer.configuration.configuration import Config
from analyzer.logger import Logger
from analyzer.database import Database
from analyzer.scheduler import SafeScheduler
from analyzer.twitter_sentiment import TweetMiner
from analyzer.notifications import NotificationHandler
from analyzer.communications.telegram_bot import TelegramBot
from analyzer.communications import utils


def main():
    config = Config()

    logger = Logger(config)

    comms = TelegramBot(logger, config)

    # comms_logger = Logger(logging_service="comms_logger")
    # logging.basicConfig(filename='./logs/'+__logger__+'.log', filemode='w')
    logger.info('Starting freqtrade ver: '+__version__)

    schedule = SafeScheduler(logger)

    cg = CoinGeckoAPI()
    loader = Loader(logger, config, cg)
    db = Database(logger, config, loader)
    processor = Processor(logger, loader, db, config)
    # miner = TweetMiner(config, logger, db)

    # Comms

    logger.info("Using CoinGecko exchange: " + config.EXCHANGE)

    if config.TGRAM_ENABLED:
        comms.send_msg('Starting freqtrade ver: '+__version__)

    schedule.every(12).hours.do(processor.check_new_coins
                                ).tag("Checking for new coins")
    schedule.every(60).minutes.do(
        processor.update_coin_data).tag("Updating coin data")

    # TODO
    # implement telegrom bot
    # prune logs
    # prune databases

    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    finally:
        exit()


# """
# Analyzer is the main module of this bot. It contains the class Analyzer()
# """

# import time
# import logging
# from typing import Any, Dict, List, Optional

# from analyzer import __version__
# from analyzer.loader import Loader
# from analyzer.processor import Processor
# from pycoingecko import CoinGeckoAPI
# from analyzer.configuration.configuration import Config
# from analyzer.logger import Logger
# from analyzer.database import Database
# from analyzer.scheduler import SafeScheduler
# from analyzer.twitter_sentiment import TweetMiner
# from analyzer.notifications import NotificationHandler
# from analyzer.communications.telegram_bot import TelegramBot
# from analyzer.communications import utils
# from analyzer.mixins.logging_mixin import LoggingMixin

# logger = logging.getLogger(__name__)


# class Analyzer(LoggingMixin):
#     """
#     Analyzer is the main class of the bot.
#     This is from here the bot start its logic.
#     """

#     def __init__(self, config: Dict[str, Any]) -> None:
#         """
#         Init all variables and objects the bot needs to work
#         :param config: configuration dict, you can use Configuration.get_config()
#         to get the config dict.
#         """


#          # Init bot state
#         self.state = State.STOPPED

# def main():
#     logger = Logger()
#     comms_logger = Logger(logging_service="comms_logger")
#     logger.info("Starting")

#     schedule = SafeScheduler(logger)

#     config = Config()
#     cg = CoinGeckoAPI()
#     loader = Loader(logger, config, cg)
#     db = Database(logger, config, loader)
#     processor = Processor(logger, loader, db, config)
#     miner = TweetMiner(config, logger, db)

#     # Comms
#     comms = TelegramBot(comms_logger, config)

#     # if config.TELEGRAM_TOKEN is None or config.TELEGRAM_CHAT_ID is None:
#     #     Utils.setup_telegram_constants()

#     # Setup update notifications scheduler
#     # self.scheduler.
#     # scheduler.enter(1, 1, utils.update_checker)
#     # time.sleep(1)
#     # scheduler.run(blocking=False)

#     logger.info("Using CoinGecko exchange: " + config.EXCHANGE)

#     if comms.enabled:
#         comms.run_bot()

#     schedule.every(12).hours.do(processor.check_new_coins
#                                 ).tag("Checking for new coins")
#     schedule.every(60).minutes.do(
#         processor.update_coin_data).tag("Updating coin data")

#     # TODO
#     # implement telegrom bot
#     # prune logs
#     # prune databases

#     try:
#         while True:
#             schedule.run_pending()
#             time.sleep(5)
#     finally:
#         exit()
