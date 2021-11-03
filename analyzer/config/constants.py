# pragma pylint: disable=too-few-public-methods

"""
bot constants
"""
import configparser
import os

from typing import List, Tuple

# Paths
DEFAULT_CONFIG_PATH = "./config/config.cfg"
CONFIG_SECTION = "configuration_data"
DB_PATH = "./data"
DB_NAME = "analyzer_db.db"
COINLIST_PATH = "./config/coins.txt"
LOGFILE_PATH = "./logs/analyzer_logfile.log"

# System
DATETIME_PRINT_FORMAT = "%Y-%m-%d %H:%M:%S"


# Notifications
DEFAULT_STATUS = "on"
DEFAULT_WARNING = "on"
DEFAULT_STARTUP = "off"

# Intervals
PROCESS_THROTTLE_SECS = 120  # sec
UPDATE_COINS = 500  # sec - 5 min
MEDIUM_THROTTLE_SEC = 3600  # 60 min
CHECK_COINS = 43200  # 12 hr
HEARTBEAT_INTERVAL = 60  # sec
NOTIFY_HEARTBEAT_INTERVAL = 300  # sec
RETRY_TIMEOUT = 30  # sec
VERBOSITY_SIMPLE = 0
VERBOSITY_DEBUG = 1
LOG_LIFE = 3 # days

# Fiat
SUPPORTED_FIAT = [
    "AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK", "DKK",
    "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
    "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN",
    "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "ZAR", "USD",
    "BTC", "ETH", "XRP", "LTC", "BCH"
]

# Define decimals per coin for outputs
# Only used for outputs.
DECIMAL_PER_COIN_FALLBACK = 3  # Should be low to avoid listing all possible FIAT's
DECIMALS_PER_COIN = {
    'BTC': 8,
    'ETH': 5,
}

DUST_PER_COIN = {
    'BTC': 0.0001,
    'ETH': 0.01
}

# self.CURRENT_COIN = os.environ.get("CURRENT_COIN") or config.get(USER_CONFIG_SECTION, "current_coin")

# def get_config(self) -> Dict[str, Any]:
#     """
#     Return the config. Use this method to get the bot config
#     :return: Dict: Bot config
#     """
#     if self.config is None:
#         self.config = self.load_config()

#     return self.config
