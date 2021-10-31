# Config consts
import configparser
import os

from ..config import constants

CONFIG_NAME = "./config/config.cfg"
CONFIG_SECTION = "configuration_data"
NOTI_SECTION = "notifications"
CREDENTIALS_NAME = "./config/credentials.cfg"
CREDENTIALS_SECTION = "credentials_data"
APPRISE_PATH = "./config/apprise.yml"
NOTIFICATIONS_ROOT = "./notifications/"


class Config:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self):
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "bridge": "USDT",
            "scout_multiplier": "5",
            "scout_sleep_time": "5",
            "hourToKeepScoutHistory": "1",
            "tld": "us",
            "strategy": "default",
            "sell_timeout": "0",
            "buy_timeout": "0",
        }

        cred_config = configparser.ConfigParser()

        if not os.path.exists(CONFIG_NAME):
            print(
                "No configuration file (user.cfg) found! See README. Assuming default config...")
            config[CONFIG_SECTION] = {}
        else:
            config.read(CONFIG_NAME)

        # Credentials config
        if not os.path.exists(CREDENTIALS_NAME):
            print(
                "No configuration file (user.cfg) found! See README. Assuming default config...")
            cred_config[CREDENTIALS_SECTION] = {}
        else:
            cred_config.read(CREDENTIALS_NAME)

        # Secrets
        self.TGRAM_TOKEN = cred_config.get(
            CREDENTIALS_SECTION, "telegram_token")
        self.TGRAM_CHAT_ID = cred_config.get(
            CREDENTIALS_SECTION, "telegram_chat_id")
        self.BINANCE_API_KEY = os.environ.get("API_KEY") or cred_config.get(
            CREDENTIALS_SECTION, "binance_api_key")
        self.BINANCE_API_SECRET_KEY = os.environ.get("API_SECRET_KEY") or cred_config.get(
            CREDENTIALS_SECTION, "binance_api_secret_key")

        # Paths
        self.LOGFILE_PATH = constants.LOGFILE_PATH
        self.DB_PATH = constants.DB_PATH
        self.COINS_PATH = constants.COINLIST_PATH
        self.TGRAM_URL = "https://api.telegram.org/bot"
        self.APPRISE_PATH = APPRISE_PATH
        self.NOTIF_ROOT_PATH = NOTIFICATIONS_ROOT

        # Notifications
        self.TGRAM_UPDATE_BROADCASTED_BEFORE = False
        self.NOTI_UPDATE_BROADCASTED_BEFORE = False
        self.TGRAM_KEYBOARD = None
        self.TGRAM_STATUS = config.get(NOTI_SECTION, "status") or constants.DEFAULT_STATUS
        self.TGRAM_WARNING = config.get(NOTI_SECTION, "warning") or constants.DEFAULT_WARNING
        self.TGRAM_STARTUP = config.get(NOTI_SECTION, "startup") or constants.DEFAULT_STARTUP

        self.TGRAM_NOTI = "on"
        if self.TGRAM_STATUS == "off" and self.TGRAM_WARNING == "off" and self.TGRAM_WARNING == "off":
            self.TGRAM_NOTI = "off"

        # APIs
        self.BINANCE_ENABLED = False
        self.TGRAM_ENABLED = False


        self.BINANCE_TLD = os.environ.get(
            "TLD") or config.get(CONFIG_SECTION, "tld")

        # Prune settings
        self.SCOUT_HISTORY_PRUNE_TIME = float(
            os.environ.get("") or config.get(
                CONFIG_SECTION, "hourToKeepScoutHistory")
        )

        # Get config for scout
        self.SCOUT_MULTIPLIER = float(
            os.environ.get("SCOUT_MULTIPLIER") or config.get(
                CONFIG_SECTION, "scout_multiplier")
        )
        

        # # Get supported coin list from the environment
        # supported_coin_list = [
        #     coin.strip() for coin in os.environ.get("SUPPORTED_COIN_LIST", "").split() if coin.strip()
        # ]
        # # Get supported coin list from supported_coin_list file
        # if not supported_coin_list and os.path.exists("supported_coin_list"):
        #     with open("supported_coin_list") as rfh:
        #         for line in rfh:
        #             line = line.strip()
        #             if not line or line.startswith("#") or line in supported_coin_list:
        #                 continue
        #             supported_coin_list.append(line)
        # self.SUPPORTED_COIN_LIST = supported_coin_list

        # self.STRATEGY = os.environ.get("STRATEGY") or config.get(
        #     CONFIG_SECTION, "strategy")

        # self.SELL_TIMEOUT = os.environ.get("SELL_TIMEOUT") or config.get(
        #     CONFIG_SECTION, "sell_timeout")
        # self.BUY_TIMEOUT = os.environ.get("BUY_TIMEOUT") or config.get(
        #     CONFIG_SECTION, "buy_timeout")
        # self.BRIDGE_SYMBOL = os.environ.get("BRIDGE_SYMBOL") or cred_config.get(CONFIG_SECTION, "bridge")
        # self.BRIDGE = Coin(self.BRIDGE_SYMBOL, False)

        # System
        self.VERBOSITY_SIMPLE = constants.VERBOSITY_SIMPLE
        self.VERBOSITY_DEBUG = constants.VERBOSITY_DEBUG
        self.INITIAL_STATE = config.get(CONFIG_SECTION, "initial_state")
        self.EXCHANGE = config.get(CONFIG_SECTION, "exchange")

        # Time
        self.HEARTBEAT_INTERVAL = constants.HEARTBEAT_INTERVAL
        self.NOTIFY_HEARTBEAT_INTERVAL = constants.NOTIFY_HEARTBEAT_INTERVAL
        self.BOT_SLEEP_TIME = int(config.get(
            constants.CONFIG_SECTION, "bot_sleep_time"))
        self.CHECK_COINS_INTERVAL = int(constants.CHECK_COINS)
        self.UPDATE_COINS_INTERVAL = int(constants.UPDATE_COINS)
        self.LOG_LIFESPAN = int(
            config.get(CONFIG_SECTION, "log_lifespan") or constants.LOG_LIFE
        )
    