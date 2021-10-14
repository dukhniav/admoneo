#!python3

import time

from analyzer.loader import Loader
from analyzer.processor import Processor
from pycoingecko import CoinGeckoAPI
from analyzer.conf.config import Config
from analyzer.logger import Logger
from analyzer.database import Database
from analyzer.scheduler import SafeScheduler


def main():
    logger = Logger()
    logger.info("Starting")

    config = Config()
    db = Database(logger, config)
    cg = CoinGeckoAPI()
    loader = Loader(logger, config, db, cg)
    processor = Processor(logger, loader, db)

    logger.info("Getting data from CoinGecko exchange: " + config.EXCHANGE)
    processor.process_coin_list()

    schedule = SafeScheduler(logger)
    schedule.every(5).minutes.do(
        processor.update_coin_values).tag("updating")
    # schedule.every(1).minutes.do(trader.update_values).tag("updating value history")
    # schedule.every(1).minutes.do(db.prune_scout_history).tag("pruning scout history")
    # schedule.every(1).hours.do(db.prune_value_history).tag("pruning value history")
    try:
        while True:
            schedule.run_pending()
            time.sleep(5)
    finally:
        exit()
