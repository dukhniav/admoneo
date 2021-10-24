#!python3
from datetime import datetime

from pycoingecko import CoinGeckoAPI as cg
from pycoingecko.api import CoinGeckoAPI

import logging
from analyzer.config import Config
from .models.coin import Coin

logger = logging.getLogger(__name__)


class Loader:
    def __init__(self, config: Config):
        self.config = config
        self.cg = CoinGeckoAPI()
        logger.info("Initializing loader...")

    def get_coins(self):
        logger.info("Getting coin values")
        coins = self.cg.get_exchanges_tickers_by_id(self.config.EXCHANGE)
        print(self.cg.get_coins_list())

        return coins

    def get_cg_exchanges(self):
        return self.cg.get_exchanges_list()

    def get_coin_list(self):
        logger.info("Getting available coins from " +
                    self.config.EXCHANGE)
        coins = self.cg.get_exchanges_tickers_by_id(self.config.EXCHANGE)
        return coins

    def get_coin_info(self, coin_name):
        # logger.info("Getting info for: "+coin_name)
        coin_data = self.cg.get_coin_by_id(coin_name)
        return coin_data

    def get_exchange_status_update(self):
        # self.cg.get_exchanges_status_updates_by_id
        raise NotImplementedError()
