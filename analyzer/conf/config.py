# Config consts
import configparser
import os

CFG_FL_NAME = "./config/user.cfg"
CFG_SECTION = "configuration_data"
COIN_FILE_PATH = "./data/coins.txt"
DB_FILE_PATH = "../data/analyzer.db"


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

        self.EXCHANGE = config.get(CFG_SECTION, "exchange")
        self.MONGO_URL = "mongodb+srv://analyzerapp:" + \
            config.get(CFG_SECTION, "mongo_pw") + \
            "@cluster0.7ejxn.mongodb.net/AnalyzerDB?retryWrites=true&w=majority"
        self.SLEEP_TIME = config.get(CFG_SECTION, "bot_sleep_time")

        # self.CURRENT_COIN = os.environ.get("CURRENT_COIN") or config.get(USER_CFG_SECTION, "current_coin")
