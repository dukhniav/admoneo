import json

from pymongo import MongoClient
from pymongo import errors
from pprint import pprint
from urllib import parse

from .conf.config import Config
from .models.coin import Coin
from .logger import Logger


class Database():
    def __init__(self, logger: Logger, config: Config):
        self.logger = logger
        self.config = config
        self.client = MongoClient(config.MONGO_URL)

        self.db = self.client.analyzerdb

    def add_new_coin(self, coin_base, coin_name):
        try:
            # Try to validate a collection
            self.db.validate_collection("coin_list")
        except errors.OperationFailure:  # If the collection doesn't exist
            self.logger.info("Creating cllection 'Coin List'")
            self.db.create_collection("coin_list")

        coin_collection = self.db.get_collection("coin_list")
        coin_collection.insert_one(
            {
                "_id": coin_base,
                "coin_name": coin_name
            }
        )

    def add_coin(self, coin: Coin):
        try:
            # Try to validate a collection
            self.db.validate_collection("coins")
        except errors.OperationFailure:  # If the collection doesn't exist
            print("INFO: Creating cllection 'Coins' ...", end='')
            self.db.create_collection("coins")

        coin_collection = self.db.get_collection("coins")
        coin_collection.insert_one(
            {"_id": coin.coin_base,
                "coin_name": coin.coin_name,
                "coin_last": coin.coin_last,
                "coin_volume": coin.coin_volume,
                "bid_ask_spread_percentage": coin.bid_ask_spread_percentage,
                "target_coin_name": coin.target_coin_name,
                "last_fetch_at": coin.last_fetch_at,
                "coin_trust": coin.coin_trust,
                "coin_anomaly": coin.coin_anomaly,
                "coin_stale": coin.coin_stale,
                "enabled": coin.enabled
             }
        )

    def coin_exists(self, coin_base):
        coin_collection = self.db.get_collection("coins")
        coin = coin_collection.find_one(
            {"_id": coin_base}, {"_id": 1})

        status = True
        if coin is None:
            status = False

        return status

    def update_coin(self, coin: Coin):
        coin_collection = self.db.get_collection("coins")
        coin_collection.find_one_and_replace(
            {'_id': coin.coin_base}, {
                {
                    "coin_last": coin.coin_last,
                    "coin_volume": coin.coin_volume,
                    "bid_ask_spread_percentage": coin.bid_ask_spread_percentage,
                    "last_fetch_at": coin.last_fetch_at,
                    "coin_trust": coin.coin_trust,
                    "coin_anomaly": coin.coin_anomaly,
                    "coin_stale": coin.coin_stale,
                }
            }
        )

    def get_coin_name(self, coin_base):
        coin_collection = self.db.get_collection("coins")
        coin = coin_collection.find_one(
            {"_id": coin_base}, {"_id": 1})

        coin_name = None
        if coin is not None:
            coin_name = coin.coin_name

        return coin_name
