#!python3

from pycoingecko import CoinGeckoAPI as cg
from pycoingecko.api import CoinGeckoAPI

from .conf.config import Config


class Loader:
    def __init__(self):
        self.config = Config()

    def get_coins(self):
        cg = CoinGeckoAPI()
        coins = cg.get_exchanges_tickers_by_id(self.config.EXCHANGE)
        return coins
