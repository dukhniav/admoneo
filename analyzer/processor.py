#!python3

import pandas as pd

from .models.coin import Coin
from .database import Database
from .loader import Loader
from .conf.config import Config
from .logger import Logger


class Processor():
    def __init__(self, logger: Logger, loader: Loader, db: Database, config: Config):
        self.logger = logger
        self.loader = loader
        self.db = db
        self.config = config

    def check_new_coins(self):
        coin_list = self.loader.get_coin_list()
        new_coin_counter = 0
        for coin in coin_list['tickers']:
            if self.db.coin_exists(coin['base']):
                continue
            else:
                new_coin_counter += 1
                self.db.add_new_coin(coin['base'], coin['coin_id'])

        if new_coin_counter > 0:
            self.logger.info("Found and added new coins on exchange")

    def update_coin_list(self):
        raise NotImplementedError()

    """
    Update coins on a scheduled basis
    """

    # def update_coin_values(self):
    #     coin_list = self.loader.get_coin_list()

    #     coin_counter = 0
    #     for coin in coin_list['tickers']:
    #         coin_counter += 1
    #         coin_pending = Coin(
    #             coin['base'],
    #             coin['coin_id'],
    #             coin_list["symbol"],
    #             coin['last'],
    #             coin['volume'],
    #             coin['bid_ask_spread_percentage'],
    #             coin['target_coin_id'],
    #             coin['last_fetch_at'],
    #             coin['trust_score'],
    #             coin['is_anomaly'],
    #             coin['is_stale'])
    #         self.db.update_coin(coin_pending)
    #     self.logger.info("Updated ", coin_counter, " coins")

    def update_coin_data(self):
        coin_list = self.db.get_all_coins()

        self.logger.info("Updating coin data")
        for coin in coin_list:
            found_exchange = False
            exchange_info = ''
            # coin_counter += 1

            coin_data = self.loader.get_coin_info(coin["coin_name"])

            for exchange in coin_data["tickers"]:
                if exchange["market"]["identifier"] == self.config.EXCHANGE and not found_exchange:
                    exchange_info = exchange
                    found_exchange = True

            coin_pending = Coin(
                exchange_info["base"],
                coin_data["id"],
                coin_data["symbol"],
                exchange_info["last"],
                exchange_info["volume"],
                exchange_info["bid_ask_spread_percentage"],
                exchange_info["target"],
                exchange_info["last_fetch_at"],
                exchange_info["trust_score"],
                exchange_info["is_anomaly"],
                exchange_info["is_stale"]
            )
            if not self.db.coin_info_exists(exchange_info["base"]):
                self.db.add_coin(coin_pending)
            else:
                self.db.update_coin(coin_pending)
