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
    # processor.process_coin_list()

    # schedule.every(5).minutes.do(
    # processor.update_coin_values).tag("updating")
    # schedule.every(1).minute.do(
    # miner.mine_crypto_currency_tweets).tag("mining")
    # logger.info("Checking for new coins...")
    # processor.check_new_coins()
    # logger.info("Getting coin data")
    #
    schedule.every(12).hours.do(processor.check_new_coins
                                ).tag("Checking for new coins")
    schedule.every(60).minutes.do(
        processor.update_coin_data).tag("Updating coin data")
    # processor.update_coin_values()
    logger.info("Mining tweets...")
    # miner.mine_crypto_currency_tweets()
    # schedule.every(1).minutes.do(trader.update_values).tag("updating value history")
    # schedule.every(1).minutes.do(db.prune_scout_history).tag("pruning scout history")
    # schedule.every(1).hours.do(db.prune_value_history).tag("pruning value history")
    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    finally:
        exit()
