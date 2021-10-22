import json

from pymongo import MongoClient
from pymongo import errors
from pprint import pprint
from urllib import parse

from .configuration.configuration import Config
from .models.coin import Coin
from .logger import Logger
from .loader import Loader


class Database():
    def __init__(self, logger: Logger, config: Config, loader: Loader):
        self.logger = logger
        self.config = config
        self.loader = loader
        self.client = MongoClient('127.0.0.1', 27017)
        self.logger.debug("Starting database...")


        # Uncomment below to use Mongo Atlas db
        # self.client = MongoClient(config.MONGO_URL)
        self.db = self.client.analyzerdb

    def add_tweet_sentiment(self, coin_base, coin_name, sentiment, timestamp):
        try:
            self.db.validate_collection("sentiment")
        except errors.OperationFailure:
            self.logger.info("Creating collection 'Sentiment'")
            self.db.create_collection("sentiment")
        coin_collection = self.db.get_collection("sentmient")
        coin_collection.insert_one(
            {
                "_id": coin_base,
                "coin_name": coin_name,
                "sentiment": sentiment,
                "last_updated": timestamp
            }
        )

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
            self.db.validate_collection("coin_info")
        except errors.OperationFailure:  # If the collection doesn't exist
            self.logger.info("Creating cllection 'Coin Info'")
            self.db.create_collection("coin_info")

        coin_collection = self.db.get_collection("coin_info")
        coin_collection.insert_one(
            {"_id": coin.coin_base,
                "coin_name": coin.coin_name,
                "coin_symbol": coin.coin_symbol,
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
        coin_collection = self.db.get_collection("coin_list")
        # self.logger.info("Checking coin: ", coin_base)
        coin = coin_collection.find_one(
            {"_id": coin_base}, {"_id": 1})

        status = True
        if coin is None:
            status = False

        return status

    def coin_info_exists(self, coin_base):
        coin_collection = self.db.get_collection("coin_info")
        coin = coin_collection.find_one(
            {"_id": coin_base}, {"_id": 1})

        status = True
        if coin is None:
            status = False

        return status

    def update_coin(self, coin: Coin):
        coin_collection = self.db.get_collection("coin_info")
        coin_collection.update_one({"_id": coin.coin_base},
                                   {"$set": {
                                       "coin_last": coin.coin_last,
                                       "coin_volume": coin.coin_volume,
                                       "bid_ask_spread_percentage": coin.bid_ask_spread_percentage,
                                       "last_fetch_at": coin.last_fetch_at,
                                       "coin_trust": coin.coin_trust,
                                       "coin_anomaly": coin.coin_anomaly,
                                       "coin_stale": coin.coin_stale,
                                   }
        }, upsert=True)

        # db.collection.update_one({"_id":"key1"}, {"$set": {"id":"key1"}}, upsert=True)

    def get_coin_name(self, coin_base):
        coin_collection = self.db.get_collection("coins")
        coin = coin_collection.find_one(
            {"_id": coin_base}, {"_id": 1})

        coin_name = None
        if coin is not None:
            coin_name = coin.coin_name

        return coin_name

    def get_all_coins(self):
        db = self.db.get_collection("coin_list")
        return list(db.find({}, {"coin_name": 1}))
