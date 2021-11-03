"""
This module contains the class to persist all operations
"""


from logging import getLogger
from typing import Any

import pandas as pd
from analyzer.config.config import Config
from analyzer.enums.tables import Table
from analyzer.models import Coin
from analyzer.models.signals import Session
from analyzer.utils.exceptions import OperationalException
from requests.sessions import session
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Time,
    create_engine,
    delete,
    desc,
    func,
    insert,
    inspect,
)
from sqlalchemy.exc import NoSuchModuleError
from sqlalchemy.orm import (
    Query,
    declarative_base,
    relationship,
    scoped_session,
    sessionmaker,
)
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.schema import UniqueConstraint

logger = getLogger(__name__)


_DECL_BASE: Any = declarative_base()
_SQL_DOCS_URL = "http://docs.sqlalchemy.org/en/latest/\
core/engines.html#database-urls"


class Database:
    def __init__(self, config: Config):
        """
        Initializes this module with the given config,
        registers all known command handlers
        and starts polling for message updates
        :param db_url: Database to use
        :param clean_open_orders: Remove open orders from the database.
        :return: None
        """
        self.config = config
        kwargs = {}
        db_url = "sqlite://" + self.config.DB_PATH

        if db_url == "sqlite://":
            kwargs.update(
                {
                    "poolclass": StaticPool,
                }
            )
        # Take care of thread ownership
        if db_url.startswith("sqlite://"):
            kwargs.update(
                {
                    "connect_args": {"check_same_thread": False},
                }
            )

        try:
            self.engine = create_engine(db_url, future=True, **kwargs)
        except NoSuchModuleError:
            raise OperationalException(
                f"Given value for db_url: '{db_url}' "
                f"is no valid database URL! (See {_SQL_DOCS_URL})"
            )

        """
        https://docs.sqlalchemy.org/en/13/orm/contextual.html#thread-local-scope
        Scoped sessions proxy requests to the appropriate thread-local session.
        We should use the scoped_session object - not a seperately initialized
        version
        Coin._session = scoped_session(sessionmaker(bind=self.engine,
        autoflush=True))
        Coin.query = Coin._session.query_property()
        """
        # previous_tables = inspect(self.engine).get_table_names()
        _DECL_BASE.metadata.create_all(self.engine)

    def create_tables(self):
        """create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        self.token_data = Table(
            "token_data",
            self.meta,
            Column("id", Integer, primary_key=True),
            Column("symbol", String),
            Column("timestamp", Time),
            Column("open", Float),
            Column("close", Float),
            Column("high", Float),
            Column("low", Float),
        )

        self.tokens = Table(
            "tokens",
            self.meta,
            Column("_id", Integer, primary_key=True),
            Column("symbol", String),
        )
        self.tokens.create(checkfirst=True)
        self.token_data.create(checkfirst=True)

    """
    Coin
    - Add
    - Delete
    - Get all coins
    - Get single coin
    - Update single coin
    """

    def add_single_coin(self, coin: Coin) -> None:
        """
        Used to add a single coin to DB
        """
        print("adding single coin")

    def add_mult_coins(self, coins: list(Coin)):
        """
        Used to add multiple coins
        """
        logger.warning("Not implemented all the way yet")
        query = {"_id": "symbol" for coin in coins}

        query = dict()

        with self.engine.connect() as conn:
            result = conn.execute(insert(self.tokens), query)
            conn.commit()

    def update_single_coin(self, coin: Coin) -> None:
        """
        Used to update a single coin
        """
        logger.warning("Not implemented")

    def update_mult_coins(self, coins: list(Coin)) -> None:
        """
        Used to update multiple coins at once
        Most likely from a list
        """
        logger.warning("Not implemented")

    def delete_single_coin(self, symbol) -> None:
        Coin.query.session.delete(self)
        Coin.commit()

    def delete_mult_coins(self, coins: list(Coin)) -> None:
        logger.warning("Not implemented")

    def fetch_coin_by_id(self, id) -> Coin:
        """
        Used to fetch a single coin from DB using its' ID
        """
        coin = self.tokens.select([self.tokens.c._id, self.tokens.c.symbol])
        coin = coin.where(self.tokens.c._id == id)
        result = session.execute(coin)
        out = result.fetchall()
        return out

    def fetch_coin_by_name(self, coin_name) -> Coin:
        """
        Used to fetch a single coin from DB using its' __name__
        """
        logger.warning("Not implemented")

    def get_all_coins(self) -> list(Coin):
        """
        Used to retrieve all coins from database
        """
        coin = self.tokens.select([self.tokens.c._id, self.tokens.c.symbol])
        result = session.execute(coin)
        out = result.fetchall()
        return out

    """
    CoinInfo
    - Add
    - Delete
    - Update
    - Add multiple
    - Update multiple
    - Get single coin info
    """

    def add_single_cd(self, df: pd.DataFrame) -> None:
        """
        Used to add coin data for a single coin
        """
        df.to_sql(name="token_data", con=self.engine, if_exists="append", index=False)

    def add_mult_cd(self, coins: list(Coin)) -> None:
        logger.warning("Not implemented")

    def update_single_cd(self, coin: Coin) -> None:
        logger.warning("Not implemented")

    def update_mult_cd(self, coins: list(Coin)) -> None:
        logger.warning("Not implemented")

    def delete_coin_data(self, coin_name: str) -> None:
        logger.warning("Not implemented")

    # def last_fetched(self, _id):
    #     last_fetched = None
    #     try:
    #         cur = self.conn.cursor()
    #         last_fetched = cur.execute(db_queries.last_fetched, (_id,))
    #     except Error as e:
    #         print(e)
    #     return last_fetched

    # def get_coin_data(self, coin_name, rows):
    #     cur = self.conn.cursor()
    #     data = cur.execute(db_queries.get_coin_data,
    #                        (coin_name, rows,)).fetchall()
    #     print(data)
    #     return data

    # def check_table_exists(self, table_name):
    #     """
    #     Check if a given table already exists.
    #     Only used in startup or when db gets deleted
    #     :param: table name
    #     :return: boolean if table exists
    #     """
    #     table_exists = True
    #     try:
    #         cur = self.conn.cursor()
    #         cur.execute(db_queries.check_table, (table_name,))
    #     except Error as e:
    #         print(e)
    #     if cur.fetchone()[0] == 0:
    #         table_exists = False
    #     return table_exists

    # def add_new_coin(self, _id, name):
    #     """
    #     Create a new project into the projects table
    #     :param conn:
    #     :param _id:
    #     :param name:
    #     :return: project id
    #     """
    #     cur = self.conn.cursor()
    #     cur.execute(db_queries.add_new_coin, (_id, name,
    #                 self.config.EXCHANGE, datetime.now(),))
    #     self.conn.commit()
    #     return cur.lastrowid

    # def check_coin_exists(self, _id) -> bool:
    #     """
    #     Checks if a coin exists
    #     """
    #     coin_exists = True
    #     cur = self.conn.cursor()
    #     cur.execute(db_queries.coin_exists, (_id,))
    #     if cur.fetchone()[0] == 0:
    #         coin_exists = False
    #     return coin_exists

    # def get_coin_list(self):
    #     """
    #     Fetch list of coins to be worked on
    #     """
    #     cur = self.conn.cursor()
    #     coin_list = cur.execute(db_queries.get_coin_list).fetchall()
    #     return coin_list

    # def add_coin_data(self, coin: Coin):
    #     """
    #     Add coin data
    #     :param coin: Coin object with data to be pushed to db
    #     :return: none
    #     """
    #     cur = self.conn.cursor()
    #     cur.execute(db_queries.add_coin_data, coin.__info__())
    #     self.conn.commit()
