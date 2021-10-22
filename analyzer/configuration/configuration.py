# Config consts
import configparser
import os
import logging
import warnings
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from analyzer.configuration import constants
from analyzer.utils.enums import runmode

CFG_FL_NAME = "./config/user.cfg"
CFG_SECTION = "configuration_data"
COIN_FILE_PATH = "./data/coins.txt"
DB_FILE_PATH = "../data/analyzer.db"
APPRISE_CONFIG_PATH = "./config/apprise.yml"

logger = logging.getLogger(__name__)


class Config:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self):
        self.config: Optional[Dict[str, Any]] = None
        self.runmode = runmode

        config = configparser.ConfigParser(strict=False, interpolation=None)
        config["DEFAULT"] = {
            "file_path": "./coins.txt"
        }

        if not os.path.exists(constants.DEFAULT_CONFIG_PATH):
            print(
                "No configuration file (config.cfg) found! See README. Assuming default config...")
            config[constants.CONFIG_SECTION] = {}
        else:
            config.read(constants.DEFAULT_CONFIG_PATH)

        # MongoDB
        self.MONGO_USERNAME = config.get(
            constants.CONFIG_SECTION, "mongo_user")
        self.MONGO_PASSWORD = config.get(
            constants.CONFIG_SECTION, "mongo_pw")

        # Twitter
        self.TWITTER_APP_NAME = config.get(
            constants.CONFIG_SECTION, "twitter_app_name")
        self.TWITTER_API_CONSUMER_KEY = config.get(
            constants.CONFIG_SECTION, "twitter_api_consumer_key")
        self.TWITTER_API_CONSUMER_SECRET = config.get(
            constants.CONFIG_SECTION, "twitter_api_consumer_secret")
        self.TWITTER_BEARER_TOKEN = config.get(
            constants.CONFIG_SECTION, "twitter_bearer_token")
        self.TWITTER_ACCESS_TOKEN = config.get(
            constants.CONFIG_SECTION, "twitter_access_token")
        self.TWITTER_ACCESS_TOKEN_SECRET = config.get(
            constants.CONFIG_SECTION, "twitter_access_token_secret")

        # Telegram
        self.TGRAM_TOKEN = config.get(
            constants.CONFIG_SECTION, "telegram_token")
        self.TGRAM_CHAT_ID = config.get(
            constants.CONFIG_SECTION, "telegram_chat_id")
        self.TGRAM_ENABLED = False

        # System
        self.BOT_SLEEP_TIME = config.get(
            constants.CONFIG_SECTION, "bot_sleep_time")

        # Data
        self.EXCHANGE = config.get(constants.CONFIG_SECTION, "exchange")

        # # News
        # self.SENTIMENT_KEY = config.get(
        #     constants.CONFIG_SECTION, "sentiment_key")
        # self.WEBSEARCH_KEY = config.get(
        #     constants.CONFIG_SECTION, "websearch_key")
