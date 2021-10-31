from enum import Enum


class Table(Enum):
    """
    Database tables
    """
    COIN = "coins"
    DATA = "coin_data"
    TWITTER = "twitter_data"

    def __str__(self):
        return f"{self.name.lower()}"
