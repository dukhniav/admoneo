# Config consts
import configparser
import os

from .models import Coin

CFG_FL_NAME = "configuration.cfg"
CFG_SECTION = "configuration_data"


class Config:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self):
        # Init config
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "bridge": "USDT",
            "scout_multiplier": "5",
            "scout_sleep_time": "5",
            "hourToKeepScoutHistory": "1",
            "tld": "com",
            "strategy": "default",
            "sell_timeout": "0",
            "buy_timeout": "0",
        }

        if not os.path.exists(CFG_FL_NAME):
            print(
                "No configuration file (user.cfg) found! See README. Assuming default config...")
            config[CFG_SECTION] = {}
        else:
            config.read(CFG_FL_NAME)

        self.BRIDGE_SYMBOL = os.environ.get(
            "BRIDGE_SYMBOL") or config.get(CFG_SECTION, "bridge")
        self.BRIDGE = Coin(self.BRIDGE_SYMBOL, False)

        # Prune settings
        self.SCOUT_HISTORY_PRUNE_TIME = float(
            os.environ.get("HOURS_TO_KEEP_SCOUTING_HISTORY") or config.get(
                CFG_SECTION, "hourToKeepScoutHistory")
        )

        # Get config for scout
        self.SCOUT_MULTIPLIER = float(
            os.environ.get("SCOUT_MULTIPLIER") or config.get(
                CFG_SECTION, "scout_multiplier")
        )
        self.SCOUT_SLEEP_TIME = int(
            os.environ.get("SCOUT_SLEEP_TIME") or config.get(
                CFG_SECTION, "scout_sleep_time")
        )

        # Get config for binance
        self.BINANCE_API_KEY = "bE2cX71hIDJlnUAGt2xTCrUVroRVLFLIjaFtAa7Wv39P2y15W1w9WbPVNfx0np1a"
        self.BINANCE_API_SECRET_KEY = "cvMCBN7lIPLn5GJAN6CybL8pKvppHucr5KcRPzGoH0a4NWpw6xbHNpsSlzU61Bvu"
        self.BINANCE_TLD = "us"

        # Get supported coin list from the environment
        supported_coin_list = [
            coin.strip() for coin in os.environ.get("SUPPORTED_COIN_LIST", "").split() if coin.strip()
        ]
        # Get supported coin list from supported_coin_list file
        if not supported_coin_list and os.path.exists("supported_coin_list"):
            with open("supported_coin_list") as rfh:
                for line in rfh:
                    line = line.strip()
                    if not line or line.startswith("#") or line in supported_coin_list:
                        continue
                    supported_coin_list.append(line)
        self.SUPPORTED_COIN_LIST = supported_coin_list

        self.CURRENT_COIN_SYMBOL = os.environ.get(
            "CURRENT_COIN_SYMBOL") or config.get(CFG_SECTION, "current_coin")

        self.STRATEGY = os.environ.get("EXCHANGE") or config.get(
            CFG_SECTION, "exchange")

        # self.SELL_TIMEOUT = os.environ.get("SELL_TIMEOUT") or config.get(
        # USER_CFG_SECTION, "sell_timeout")
        # self.BUY_TIMEOUT = os.environ.get("BUY_TIMEOUT") or config.get(
        # USER_CFG_SECTION, "buy_timeout")
