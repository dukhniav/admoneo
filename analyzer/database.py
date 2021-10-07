import sqlite3

connection = sqlite3.connect("orion.db")

cursor = connection.cursor()
cursor.execute(
    "CREATE TABLE fish (coin TEXT, species TEXT, tank_number INTEGER)")
