from sqlalchemy import Boolean, Column, String
from sqlalchemy.sql.sqltypes import Date, Float

from .base import Base


class Coin(Base):
    __tablename__ = "coins"
    coin_base = Column(String, primary_key=True)
    coin_name = Column(String)
    coin_symbol = Column(String)
    coin_last = Column(Float)
    coin_volume = Column(Float)
    bid_ask_spread_percentage = Column(Float)
    target_coin_name = Column(String)
    last_fetch_at = Column(Date)
    coin_trust = Column(String)
    coin_anomaly = Column(Boolean)
    coin_stale = Column(Boolean)
    enabled = Column(Boolean)

    def __init__(self, coin_base, coin_name, coin_symbol, coin_last, coin_volume, bid_ask_spread_percentage, target_coin_name, last_fetch_at,
                 coin_trust, coin_anomaly, coin_stale,  enabled=True):
        self.coin_base = coin_base
        self.coin_name = coin_name
        self.coin_symbol = coin_symbol
        self.coin_last = coin_last
        self.coin_volume = coin_volume
        self.bid_ask_spread_percentage = bid_ask_spread_percentage
        self.target_coin_name = target_coin_name
        self.last_fetch_at = last_fetch_at
        self.coin_trust = coin_trust
        self.coin_anomaly = coin_anomaly
        self.coin_stale = coin_stale
        self.enabled = enabled

    def __update__(self, coin_base, coin_last, coin_volume, bid_ask_spread_percentage, last_fetch_at,
                   coin_trust, coin_anomaly, coin_stale):
        self.coin_base = coin_base
        self.coin_last = coin_last
        self.coin_volume = coin_volume
        self.bid_ask_spread_percentage = bid_ask_spread_percentage
        self.last_fetch_at = last_fetch_at
        self.coin_trust = coin_trust
        self.coin_anomaly = coin_anomaly
        self.coin_stale = coin_stale

    def __info__(self):
        return (self.coin_base,
                self.coin_name,
                self.coin_symbol,
                self.coin_last,
                self.coin_volume,
                self.bid_ask_spread_percentage,
                self.target_coin_name,
                self.last_fetch_at,
                self.coin_trust,
                self.coin_anomaly,
                self.coin_stale,
                self.enabled)

    def __repr__(self):
        return f"[{self.coin_name}]"

    def __status__(self):
        return self.enabled
