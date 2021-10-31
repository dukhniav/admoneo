from sqlalchemy import Table, Column, Integer, String, MetaData,Float
from sqlalchemy.sql.sqltypes import Time
meta = MetaData()

coin_data = Table(
   'token_data', meta, 
   Column('id', Integer, primary_key = True), 
   Column('symbol', String), 
   Column('timestamp', Time),
   Column('open', Float), 
   Column('close', Float),
   Column('high', Float),
   Column('low')
)


create_coin_list_table = """ CREATE TABLE IF NOT EXISTS coins(
                                        _id text PRIMARY KEY,
                                        coin_name text NOT NULL,
                                        exchange text,
                                        date_added text                                  
                            ); """

create_coin_data_table = """ CREATE TABLE IF NOT EXISTS coin_data (
                                        _id integer PRIMARY KEY,
                                        coin_base text,
                                        coin_name text NOT NULL, 
                                        coin_symbol text,  
                                        coin_last real,
                                        coin_volume real,  
                                        bid_ask_spread_percentage real,
                                        target_coin_name text,
                                        last_fetch_at text,
                                        coin_trust integer, 
                                        coin_anomaly integer,  
                                        coin_stale integer,
                                        enabled integer
                                    ); """

check_table = """select exists(SELECT name FROM sqlite_master WHERE type='table' AND name=?);"""

add_new_coin = ''' INSERT INTO coins(_id,coin_name, exchange, date_added) VALUES(?,?,?,?);'''

coin_exists = """SELECT EXISTS(
                    SELECT 1 
                    FROM coins 
                    WHERE coin_base=?);"""

last_fetched = """SELECT last_fetch_at 
                    FROM coin_data 
                    WHERE coin_base = ?);"""

get_coin_data = """select * from coin_data where coin_name = ? order by last_fetch_at desc limit ?; """

add_coin_data = """INSERT INTO coin_data (
                    coin_base,
                    coin_name,
                    coin_symbol,  
                    coin_last,
                    coin_volume,  
                    bid_ask_spread_percentage,
                    target_coin_name,
                    last_fetch_at,
                    coin_trust, 
                    coin_anomaly,  
                    coin_stale,
                    enabled
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?);"""

get_coin_name = """SELECT coin_name 
                    FROM coins
                    WHERE _id = ?"""

get_coin_list = """ SELECT coin_name
                    FROM coins"""
