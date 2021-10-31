from datetime import datetime
from logging import getLogger
from .enums.tables import Table
from .config.config import Config
from .models import *  # pylint: disable=wildcard-import
import pandas as pd

from sqlalchemy import *

logger = getLogger(__name__)


class Database:
    def __init__(self,  config: Config):
        self.config = config
        self.create_db()

    def create_db(self):
        logger.info("Attempting to create db")
        self.engine = create_engine('sqlite:///' + self.config.DB_PATH, echo=False)
        self.meta = MetaData(self.engine)    
        self.create_tables()

    def add_coin_data(self, df: pd.DataFrame):
        df.to_sql(name = 'token_data', con = self.engine, if_exists = 'append', index=False)

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

    def create_tables(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        self.token_data = Table(
            'token_data', self.meta, 
            Column('id', Integer, primary_key = True), 
            Column('symbol', String), 
            Column('timestamp', Time),
            Column('open', Float), 
            Column('close', Float),
            Column('high', Float),
            Column('low', Float)
        )
        self.token_data.create(checkfirst=True)

        

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
