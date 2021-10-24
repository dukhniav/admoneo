#!python3

import pandas as pd
import logging

from .models.coin import Coin
from .database import Database
from .loader import Loader
from .config import Config
from pycoingecko import CoinGeckoAPI

from analyzer.models import coin

logger = logging.getLogger(__name__)


class Processor():
    def __init__(self, loader: Loader, db: Database, config: Config):
        logger.info("Initializing Processor...")
        self.loader = loader
        self.db = db
        self.config = config
        self.cg = CoinGeckoAPI()

    def get_cg_exchanges(self):
        exchanges = self.loader.get_cg_exchanges()
        df = pd.DataFrame(exchanges, columns=[
                          'id', 'name', 'trust_score', 'trust_score_rank'])
        df.set_index('name', inplace=True)
        exchanges = self.cg.get_exchanges_list()

    def check_new_coins(self):
        logger.info("Checking new coins")
        coin_list = self.loader.get_coin_list()
        new_coin_counter = 0
        for coin in coin_list['tickers']:
            if self.db.check_coin_exists(coin['base']):
                # logger.info("Coin " + coin['base'] + " exists")
                continue
            else:
                new_coin_counter += 1
                logger.info("Adding coin " + coin['coin_id'])
                self.db.add_new_coin(
                    coin['base'], coin['coin_id'])

        if new_coin_counter > 0:
            logger.info("Found and added " + new_coin_counter.__str__() +
                        " new coins on exchange")

    def load_coin_list(self):
        fp = self.config.COINS_PATH
        with open(fp) as f:
            lines = f.readlines()
        coin_list = [line.rstrip() for line in lines]
        print(coin_list)
        return coin_list

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
    #     logger.info("Updated ", coin_counter, " coins")

    def update_coin_data(self):
        """
        Add time series coin data
        """

        coin_list = self.db.get_coin_list()
        for coin in coin_list:
            found_exchange = False
            exchange_info = ''
            # coin_counter += 1

            coin_data = self.loader.get_coin_info(coin[0])

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
            self.db.add_coin_data(coin_pending)

    def update_coin_data_from_list(self, coin_list):
        """
        Add time series coin data
        """
        logger.info("Updating coin data")

        for coin in coin_list:
            logger.info(f"updating {coin}")
            found_exchange = False
            exchange_info = ''
            # coin_counter += 1

            coin_data = self.loader.get_coin_info(coin)

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
            self.db.add_coin_data(coin_pending)
