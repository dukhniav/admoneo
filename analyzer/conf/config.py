# Config consts
import configparser
import os

CFG_FL_NAME = "../config/user.cfg"
CFG_SECTION = "configuration_data"
COIN_FILE_PATH = "./data/coins.txt"
DB_FILE_PATH = "../data/analyzer.db"
# COIN_FILE_PATH = "./coins.txt"


class Config:  # pylint: disable=too-few-public-methods,too-many-instance-attributes
    def __init__(self):
        # Init config
        config = configparser.ConfigParser()
        config["DEFAULT"] = {
            "file_path": "./coins.txt"
        }
        if not os.path.exists(CFG_FL_NAME):
            print(
                "No configuration file (user.cfg) found! See README. Assuming default config...")
            config[CFG_SECTION] = {}
        else:
            config.read(CFG_FL_NAME)

        self.FILE_PATH = COIN_FILE_PATH
        self.DB_PATH = DB_FILE_PATH
        self.CREATE_COIN_TABLE_QUERY = """ CREATE TABLE IF NOT EXISTS coins (
                                        coin_base text PRIMARY KEY,
                                        coin_id text NOT NULL,
                                        coin_last real, 
                                        coin_volume real, 
                                        bid_ask_spread_percentage real, 
                                        target_coin_id text, 
                                        last_fetch_at text, 
                                        coin_trust text, 
                                        coin_anomaly integer, 
                                        coin_stale integer, 
                                        enabled integer
                                ); """
# oin.coin_base <class 'str'>
# coin.coin_name <class 'str'>
# coin.coin_last <class 'float'>
# coin.coin_volume <class 'float'>
# coin.bid_ask_spread_percentage <class 'float'>
# coin.target_coin_name <class 'str'>
# coin.last_fetch_at <class 'str'>
# coin.coin_trust <class 'str'>
# coin.coin_anomaly <class 'bool'>
# coin.coin_stale <class 'bool'>
# coin.enabled <class 'bool'>

        self.CHECK_COIN_QUERY = """ SELECT coin_base FROM coins WHERE coin_base = (?) """
        self.ADD_COIN_QUERY = ''' INSERT INTO coins(
                                        coin_base,
                                        coin_id,
                                        coin_last, 
                                        coin_volume, 
                                        bid_ask_spread_percentage, 
                                        target_coin_id, 
                                        last_fetch_at, 
                                        coin_trust, 
                                        coin_anomaly, 
                                        coin_stale, 
                                        enabled) 
                                    VALUES(?,?,?,?,?,?,?,?,?,?,?); '''

        self.EXCHANGE = config.get(CFG_SECTION, "exchange")

        # Get supported coin list from the environment
        # supported_coin_list = [
        # coin.strip() for coin in os.environ.get("SUPPORTED_COIN_LIST", "").split() if coin.strip()
        # ]
        # Get supported coin list from supported_coin_list file
        # if not supported_coin_list and os.path.exists("supported_coin_list"):
        # with open("supported_coin_list") as rfh:
        # for line in rfh:
        # line = line.strip()
        # if not line or line.startswith("#") or line in supported_coin_list:
        # continue
        # supported_coin_list.append(line)
        # self.SUPPORTED_COIN_LIST = supported_coin_list
        # self.CURRENT_COIN_SYMBOL = os.environ.get(
        # "CURRENT_COIN_SYMBOL") or config.get(USER_CFG_SECTION, "current_coin")

        # self.STRATEGY = os.environ.get("STRATEGY") or config.get(
        # USER_CFG_SECTION, "strategy")

        # self.SELL_TIMEOUT = os.environ.get("SELL_TIMEOUT") or config.get(
        # USER_CFG_SECTION, "sell_timeout")
        # self.BUY_TIMEOUT = os.environ.get("BUY_TIMEOUT") or config.get(
        # USER_CFG_SECTION, "buy_timeout")
