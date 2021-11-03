from logging import getLogger
from typing import Any

# from analyzer.config.config import Config
# from analyzer.utils.exceptions import OperationalException
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

# from .base import Base

logger = getLogger(__name__)

_DECL_BASE: Any = declarative_base()
_SQL_DOCS_URL = "http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls"


# def init_db(self, config: Config):
#     kwargs = {}

#     db_url = config.DB_PATH

#     # Take care of thread ownership
#     if db_url.startswith('sqlite://'):
#         kwargs.update({
#             'connect_args': {'check_same_thread': False},
#         })

#     try:
#         engine = create_engine(db_url, future=True, **kwargs)
#     except NoSuchModuleError:
#         raise OperationalException(f"Given value for db_url: '{db_url}' "
#                                    f"is no valid database URL! (See {_SQL_DOCS_URL})")

#     # https://docs.sqlalchemy.org/en/13/orm/contextual.html#thread-local-scope
#     # Scoped sessions proxy requests to the appropriate thread-local session.
#     # We should use the scoped_session object - not a seperately initialized version
#     Coin._session = scoped_session(sessionmaker(bind=engine, autoflush=True))


#     Trade.query = Trade._session.query_property()
#     Order.query = Trade._session.query_property()
#     PairLock.query = Trade._session.query_property()

#     previous_tables = inspect(engine).get_table_names()
#     _DECL_BASE.metadata.create_all(engine)
#     check_migrate(engine, decl_base=_DECL_BASE, previous_tables=previous_tables)


class Coin(_DECL_BASE):

    __tablename__ = "coins"

    id = Column(Integer, primary_key=True)
    symbol = Column(
        String(25), ForeignKey("coin_info.symbol"), nullable=False, index=True
    )
    active = Column(Boolean, nullable=False, default=True, index=True)

    def __init__(self, symbol, enabled=True):
        self.symbol = symbol
        self.enabled = enabled

    def __add__(self, other):
        if isinstance(other, str):
            return self.symbol + other
        if isinstance(other, Coin):
            return self.symbol + other.symbol
        raise TypeError(
            f"unsupported operand type(s) for +: 'Coin' and '{type(other)}'"
        )

    def __repr__(self):
        return f"Id={self.id}, symbol={self.symbol}"

    def info(self):
        return {"symbol": self.symbol, "enabled": self.enabled}


# class Coin():
#     def __init__(self,
#             coin_base,
#             coin_name,
#             coin_symbol,
#             coin_last,
#             coin_volume,
#             bid_ask_spread_percentage,
#             target_coin_name,
#             last_fetch_at,
#             coin_trust,
#             coin_anomaly,
#             coin_stale,
#             enabled=True):
#         self.coin_base = coin_base
#         self.coin_name = coin_name
#         self.coin_symbol = coin_symbol
#         self.coin_last = coin_last
#         self.coin_volume = coin_volume
#         self.bid_ask_spread_percentage = bid_ask_spread_percentage
#         self.target_coin_name = target_coin_name
#         self.last_fetch_at = last_fetch_at
#         self.coin_trust = coin_trust
#         self.coin_anomaly = coin_anomaly
#         self.coin_stale = coin_stale
#         self.enabled = enabled

#     def __update__(self, coin_base, coin_last, coin_volume, bid_ask_spread_percentage, last_fetch_at,
#                    coin_trust, coin_anomaly, coin_stale):
#         self.coin_base = coin_base
#         self.coin_last = coin_last
#         self.coin_volume = coin_volume
#         self.bid_ask_spread_percentage = bid_ask_spread_percentage
#         self.last_fetch_at = last_fetch_at
#         self.coin_trust = coin_trust
#         self.coin_anomaly = coin_anomaly
#         self.coin_stale = coin_stale

#     def __info__(self):
#         return (self.coin_base,
#                 self.coin_name,
#                 self.coin_symbol,
#                 self.coin_last,
#                 self.coin_volume,
#                 self.bid_ask_spread_percentage,
#                 self.target_coin_name,
#                 self.last_fetch_at,
#                 self.coin_trust,
#                 self.coin_anomaly,
#                 self.coin_stale,
#                 self.enabled)

#     def __repr__(self):
#         return f"[{self.coin_name}]"

#     def __status__(self):
#         return self.enabled
