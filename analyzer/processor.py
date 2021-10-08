#!python3

from .models.coin import Coin
from .database import Database
from .loader import Loader
from .conf.config import Config


class Processor():
    def __init__(self):
        print("Initializing processor...")

    def process_coin_list(self):
        load = Loader()
        db = Database()

        coins = load.get_coins()

        coin_counter = 0
        coins_added_counter = 0
        for x in coins['tickers']:
            coin_counter += 1

            if not db.coin_exists(x['base']):
                coins_added_counter += 1
                coin = Coin(
                    x['base'],
                    x['coin_id'],
                    x['last'],
                    x['volume'],
                    x['bid_ask_spread_percentage'],
                    x['target_coin_id'],
                    x['last_fetch_at'],
                    x['trust_score'],
                    x['is_anomaly'],
                    x['is_stale'])
                db.add_coin(coin)

        print("INFO: Processed ", coin_counter,
              " coins, added ", coins_added_counter, "...")
