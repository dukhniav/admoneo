#!python3
import asyncio
import pandas as pd
import logging
import time
from pandas.core.frame import DataFrame
import json
from analyzer.models.coin import Coin
from analyzer.database import Database
from analyzer.loader import Loader
from urllib.request import urlopen
from analyzer.config.config import Config
from pycoingecko import CoinGeckoAPI
from analyzer.notifications import Telegram
import ccxt

from .models.coin import Coin

logger = logging.getLogger(__name__)


class Processor():
    def __init__(self, config: Config,  db: Database, chatbot: Telegram):
        self.chatbot = chatbot
        self.config = config
        self.db = db
        self.ccxt = ccxt.coinmarketcap()
        self.timeframe = '5m'
        self.inf_1h = '1h'

        self.rows = 2
        self.api1 = "https://api.coingecko.com/api/v3/coins/"
        self.api2 = "/ohlc?vs_currency=usd&days=1"
        self.coin_list = self.load_coin_list()
        self.db.add_coins(self.coin_list)

    def gen_signals(self, symbol):
        link = self.api1 + symbol + self.api2
        f = urlopen(link)
        data = f.read()
        df = pd.DataFrame(json.loads(data))
        df.columns = ['timestamp', 'open', 'high', 'low', 'close']
        df["symbol"] = symbol
        self.db.add_coin_data(df)

    # def get_coin_data(self, coin) -> DataFrame:
    #     data = self.db.get_coin_data(coin, self.rows)
    #     df = pd.DataFrame(data)
    #     return df

    def load_coin_list(self):
        fp = self.config.COINS_PATH
        with open(fp) as f:
            lines = f.readlines()
        coin_list = [line.rstrip() for line in lines]
        return coin_list

    def status_alert(self, msg):
        self.chat_bot.send_msg(msg)

    # def get_cg_exchanges(self):
    #     exchanges = self.loader.get_cg_exchanges()
    #     df = pd.DataFrame(exchanges, columns=[
    #                       'id', 'name', 'trust_score', 'trust_score_rank'])
    #     df.set_index('name', inplace=True)
    #     exchanges = self.cg.get_exchanges_list()

    # def check_new_coins(self):
    #     logger.info("Checking new coins")
    #     new_coin_counter = 0
    #     for coin in self.coin_list['tickers']:
    #         if self.db.check_coin_exists(coin['base']):
    #             # logger.info("Coin " + coin['base'] + " exists")
    #             continue
    #         else:
    #             new_coin_counter += 1
    #             logger.info("Adding coin " + coin['coin_id'])
    #             self.db.add_new_coin(
    #                 coin['base'], coin['coin_id'])

    #     if new_coin_counter > 0:
    #         logger.info("Found and added " + new_coin_counter.__str__() +
    #                     " new coins on exchange")

    # def update_coin_list(self):
    #     raise NotImplementedError()

    # def update_coin_data(self):
    #     """
    #     Add time series coin data
    #     """

    #     for coin in self.coin_list:
    #         found_exchange = False
    #         exchange_info = ''
    #         # coin_counter += 1

    #         coin_data = self.loader.get_coin_info(coin[0])

    #         for exchange in coin_data["tickers"]:
    #             if exchange["market"]["identifier"] == self.config.EXCHANGE and not found_exchange:
    #                 exchange_info = exchange
    #                 found_exchange = True

    #         coin_pending = self.load_coin(exchange_info, coin_data)
    #         self.db.add_coin_data(coin_pending)

    # def load_coin(self, exchange_info, coin_data):
    #     coin_pending = Coin(
    #         exchange_info["base"],
    #         coin_data["id"],
    #         coin_data["symbol"],
    #         exchange_info["last"],
    #         exchange_info["volume"],
    #         exchange_info["bid_ask_spread_percentage"],
    #         exchange_info["target"],
    #         exchange_info["last_fetch_at"],
    #         exchange_info["trust_score"],
    #         exchange_info["is_anomaly"],
    #         exchange_info["is_stale"]
    #     )

    #     return coin_pending

    def update_coin_list_data(self) -> None:
        logger.info("Updating coins")

        for coin in self.coin_list:
            self.gen_signals(coin)
        logger.info("Done iterating coin list")

    # def update_coin_data_from_list(self, coin) -> None:
    #     """
    #     Add time series coin data
    #     """

    #     logger.info(f"Updating coin data: {coin}")

    #     found_exchange = False

    #     exchange_info = ''

    #     coin_data = self.loader.get_coin_info(coin)

    #     for exchange in coin_data["tickers"]:
    #         if exchange["market"]["identifier"] == self.config.EXCHANGE and not found_exchange:
    #             exchange_info = exchange
    #             found_exchange = True

    #     coin_pending = Coin(
    #         exchange_info["base"],
    #         coin_data["id"],
    #         coin_data["symbol"],
    #         exchange_info["last"],
    #         exchange_info["volume"],
    #         exchange_info["bid_ask_spread_percentage"],
    #         exchange_info["target"],
    #         exchange_info["last_fetch_at"],
    #         exchange_info["trust_score"],
    #         exchange_info["is_anomaly"],
    #         exchange_info["is_stale"]
    #     )
    #     self.db.add_coin_data(coin_pending)
    #     time.sleep(5)
