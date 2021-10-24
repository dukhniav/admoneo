import json
import os
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import List, Optional, Union

import sqlite3
from sqlite3 import Error
from datetime import datetime
from sqlite3 import Error
from sqlite3.dbapi2 import Connection
from .models.coin import Coin

import logging
from .loader import Loader
from .utils.enums.tables import Table
from analyzer.utils import db_queries
from analyzer.communications.telegram_bot import TelegramBot

from analyzer.config import Config
from .models import *  # pylint: disable=wildcard-import

logger = logging.getLogger(__name__)

class Database():
    def __init__(self, t_gram: TelegramBot, loader: Loader, config: Config):
        self.config = config
        self.loader = loader
        self.tgram = t_gram
        logger.info("Initializing database...")
        self.create_db()

    def create_db(self):
        self.conn = self.create_connection()
        if self.conn is not None:
            # Create tables
            for table in Table:
                self.create_table(table)
        else:
            logger.debug("Error! Cannot create the database connection.")

    def send_update(self, msg):
        if not self.config.TGRAM_ENABLED():
            return

        self.tgram.send_msg(msg)
        # self.socketio_client.emit(
        #     "update",
        #     {"table": model.__tablename__, "data": model.info()},
        #     namespace="/backend",
        # )


    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        db_path = self.config.DB_PATH
        conn = None
        try:
            conn = sqlite3.connect(db_path)
            return conn
        except Error as e:
            print(e)

        return conn

    def check_table_exists(self, table_name):
        table_exists = True
        try:
            cur = self.conn.cursor()
            cur.execute(db_queries.check_table, (table_name,))
        except Error as e:
            print(e)
        if cur.fetchone()[0] == 0:
            table_exists = False
        return table_exists

    def create_table(self, table: Table):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        table_exists = self.check_table_exists(table.__str__())

        try:
            cur = self.conn.cursor()
            if table == Table.COIN and not table_exists:
                logger.info("Creating '" + table.__str__() + "' table")
                cur.execute(db_queries.create_coin_list_table)
            elif table == Table.DATA and not table_exists:
                logger.info("Creating '" + table.__str__() + "' table")
                cur.execute(db_queries.create_coin_data_table)
            elif table == table.TWITTER and not table_exists:
                logger.warning("Twitter query not implemented")
            else:
                logger.info("Table " + table.__str__() + " already exists")
        except Error as e:
            print(e)

    def add_new_coin(self, _id, name):
        """
        Create a new project into the projects table
        :param conn:
        :param _id:
        :param name:
        :return: project id
        """
        cur = self.conn.cursor()
        cur.execute(db_queries.add_new_coin, (_id, name,
                    self.config.EXCHANGE, datetime.now(),))
        self.conn.commit()
        return cur.lastrowid

    def check_coin_exists(self, _id) -> bool:
        coin_exists = True
        cur = self.conn.cursor()
        cur.execute(db_queries.coin_exists, (_id,))
        if cur.fetchone()[0] == 0:
            coin_exists = False
        return coin_exists

    def get_coin_list(self):
        cur = self.conn.cursor()
        coin_list = cur.execute(db_queries.get_coin_list).fetchall()
        return coin_list

    def add_coin_data(self, coin: Coin):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param coin:
        :return: last row
        """
        cur = self.conn.cursor()
        cur.execute(db_queries.add_coin_data, coin.__info__())
        self.conn.commit()
