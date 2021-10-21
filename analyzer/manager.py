#!python3

import time

from analyzer.loader import Loader
from analyzer.processor import Processor
from pycoingecko import CoinGeckoAPI
from analyzer.conf.config import Config
from analyzer.logger import Logger
from analyzer.database import Database
from analyzer.scheduler import SafeScheduler
from analyzer.twitter_sentiment import TweetMiner


def main():
    logger = Logger()
    logger.info("Starting")

    schedule = SafeScheduler(logger)

    config = Config()
    cg = CoinGeckoAPI()
    loader = Loader(logger, config, cg)
    db = Database(logger, config, loader)
    processor = Processor(logger, loader, db, config)
    miner = TweetMiner(config, logger, db)

    logger.info("Using CoinGecko exchange: " + config.EXCHANGE)

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
