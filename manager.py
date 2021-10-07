# #!python3

#!python3
from analyzer.loader import Loader
from analyzer.processor import Processor
from pycoingecko import CoinGeckoAPI
from analyzer.conf.config import Config


def main():
    processor = Processor()
    config = Config()

    print("INFO: Using CoinGecko exchange: ", config.EXCHANGE)
    print("INFO: Processing coins...", end='')
    processor.process_coin_list()
    print("Done")


# import time

# from analyzer.binance_api_manager import BinanceAPIManager
# from analyzer.config import Config
# from analyzer.database import Database
# from analyzer.logger import Logger
# from analyzer.scheduler import SafeScheduler
# from analyzer.strategies import get_strategy


# def main():
#     logger = Logger()
#     logger.info("Starting")

#     config = Config()
#     db = Database(logger, config)
#     manager = BinanceAPIManager(config, db, logger)
#     # check if we can access API feature that require valid config
#     try:
#         _ = manager.get_account()
#     except Exception as e:  # pylint: disable=broad-except
#         logger.error(
#             "Couldn't access Binance API - API keys may be wrong or lack sufficient permissions")
#         logger.error(e)
#         return
#     strategy = get_strategy(config.STRATEGY)
#     if strategy is None:
#         logger.error("Invalid strategy name")
#         return
#     trader = strategy(manager, db, logger, config)
#     logger.info(f"Chosen strategy: {config.STRATEGY}")

#     logger.info("Creating database schema if it doesn't already exist")
#     db.create_database()

#     db.set_coins(config.SUPPORTED_COIN_LIST)
#     db.migrate_old_state()

#     trader.initialize()

#     schedule = SafeScheduler(logger)
#     schedule.every(config.SCOUT_SLEEP_TIME).seconds.do(
#         trader.scout).tag("scouting")
#     schedule.every(1).minutes.do(
#         trader.update_values).tag("updating value history")
#     schedule.every(1).minutes.do(
#         db.prune_scout_history).tag("pruning scout history")
#     schedule.every(1).hours.do(db.prune_value_history).tag(
#         "pruning value history")
#     try:
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#     finally:
#         manager.stream_manager.close()
