#!python3
from datetime import datetime

from pycoingecko import CoinGeckoAPI as cg
from pycoingecko.api import CoinGeckoAPI

from .logger import Logger
from .conf.config import Config
from .database import Database


class Loader:
    def __init__(self, logger: Logger, config: Config, database: Database, coingecko: CoinGeckoAPI):
        self.config = config
        self.logger = logger
        self.db = database
        self.cg = coingecko

    def get_coins(self):
        self.logger.info("Getting coin values")
        coins = self.cg.get_exchanges_tickers_by_id(self.config.EXCHANGE)
        return coins

    def get_coin_list(self):
        self.logger.info("Getting available coins from ", self.config.EXCHANGE)
        coins = self.cg.get_exchanges_tickers_by_id(self.config.EXCHANGE)
        return coins

    def get_exchange_status_update(self):
        # self.cg.get_exchanges_status_updates_by_id
        raise NotImplementedError()
