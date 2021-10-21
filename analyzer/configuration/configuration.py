# Config consts
import configparser
import os

CFG_FL_NAME = "./config/user.cfg"
CFG_SECTION = "configuration_data"
COIN_FILE_PATH = "./data/coins.txt"
DB_FILE_PATH = "../data/analyzer.db"
APPRISE_CONFIG_PATH = "./config/apprise.yml"


class Config:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self):
        # Init config
        config = configparser.ConfigParser(strict=False, interpolation=None)
        config["DEFAULT"] = {
            "file_path": "./coins.txt"
        }
        config["APPRRISE"] = {"file_path": APPRISE_CONFIG_PATH}

        if not os.path.exists(CFG_FL_NAME):
            print(
                "No configuration file (user.cfg) found! See README. Assuming default config...")
            config[CFG_SECTION] = {}
        else:
            config.read(CFG_FL_NAME)

        # Data
        self.EXCHANGE = config.get(CFG_SECTION, "exchange")

        # News
        self.SENTIMENT_KEY = config.get(CFG_SECTION, "sentiment_key")
        self.WEBSEARCH_KEY = config.get(CFG_SECTION, "websearch_key")

        # Twitter
        self.TWITTER_CONSUMER_KEY = config.get(
            CFG_SECTION, "twitter_api_consumer_key")
        self.TWITTER_CONSUMER_SECRET = config.get(
            CFG_SECTION, "twitter_api_consumer_secret")
        self.TWITTER_BEARER_TOKEN = config.get(
            CFG_SECTION, "twitter_bearer_token")
        self.TWITTER_ACCESS_KEY = config.get(
            CFG_SECTION, "twitter_access_token")
        self.TWITTER_ACCESS_SECRET = config.get(
            CFG_SECTION, "twitter_access_token_secret")

        # Notifications
        self.TELEGRAM_TOKEN = None
        self.TELEGRAM_CHAT_ID = None
        self.APPRISE_CONFIG_PATH = APPRISE_CONFIG_PATH

        # Fiat
        self.SUPPORTED_FIAT = [
            "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
            "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
            "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
            "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD",
            "BTC", "ETH", "XRP", "LTC", "BCH"
        ]

        # self.CURRENT_COIN = os.environ.get("CURRENT_COIN") or config.get(USER_CFG_SECTION, "current_coin")
