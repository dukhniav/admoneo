#!python3
from pycoingecko import CoinGeckoAPI
from pycoingecko.api import CoinGeckoAPI
from logging import getLogger

from .config.config import Config

logger = getLogger(__name__)

class Loader:
    def __init__(self, config: Config):
        self.cg = CoinGeckoAPI()
        self.config = config
    
    def initialize(self):
        super()

    def get_coins(self):
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
        coin_data = self.cg.get_coin_by_id(coin_name)
        return coin_data

    def get_exchange_status_update(self):
        # self.cg.get_exchanges_status_updates_by_id
        raise NotImplementedError()
