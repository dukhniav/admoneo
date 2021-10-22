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

# System
PROCESS_THROTTLE_SECS = 5  # sec

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
