#!python3

from .models.coin import Coin
from .database import Database
from .loader import Loader
from .conf.config import Config
from .logger import Logger


class Processor():
    def __init__(self, logger: Logger, loader: Loader, db: Database):
        self.logger = logger
        self.loader = loader
        self.db = db

    def check_new_coins(self):
        coin_list = self.loader.get_coin_list()
        new_coin_counter = 0
        for coin in coin_list['tickers']:
            if not self.db.coin_exists(coin['base']):
                new_coin_counter += 1
                self.db.add_new_coin(coin['base'], coin['coin_id'])

        if new_coin_counter > 0:
            self.logger.info("Found new coins on exchange")
            return True
        else:
            return False

    def update_coin_list(self):
        raise NotImplementedError()

    """
    Update coins on a scheduled basis
    """

    def update_coin_values(self):
        coin_list = self.loader.get_coin_list()
        coin_counter = 0
        for coin in coin_list['tickers']:
            coin_counter += 1
            coin_pending = Coin(
                coin['base'],
                coin['last'],
                coin['volume'],
                coin['bid_ask_spread_percentage'],
                coin['last_fetch_at'],
                coin['trust_score'],
                coin['is_anomaly'],
                coin['is_stale'])
            self.db.update_coin(coin_pending)
        self.logger.info("Updated ", coin_counter, " coins")

    def process_coin_list(self):
        coin_list = self.loader.get_coins()

        coin_counter = 0
        coins_added_counter = 0
        for coin in coin_list['tickers']:
            coin_counter += 1

            if not self.db.coin_exists(coin['base']):
                coins_added_counter += 1
                coin_pending = Coin(
                    coin['base'],
                    coin['coin_id'],
                    coin['last'],
                    coin['volume'],
                    coin['bid_ask_spread_percentage'],
                    coin['target_coin_id'],
                    coin['last_fetch_at'],
                    coin['trust_score'],
                    coin['is_anomaly'],
                    coin['is_stale'])
                self.db.add_coin(coin_pending)

        self.logger.info("Processed " + str(coin_counter) +
                         " tokens, added " + str(coins_added_counter))
