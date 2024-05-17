import os
import sqlite3

from candle import Candle
from etl import get_project_root
from typing import List


def open_database(database_name: str, create_table: bool = True) -> sqlite3.Connection:
    path = os.path.join(get_project_root(), f"data/database/{database_name}")
    connection = sqlite3.connect(path)
    

    if create_table:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS price(
            ticker TEXT NOT NULL, 
            date TEXT NOT NULL, 
            price REAL NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume REAL NOT NULL,
            PRIMARY KEY (ticker, date)
            )"""
        )
    return connection

def insert_candles(connection: sqlite3.Connection, candles: List[Candle]):
    cursor = connection.cursor()
    data_to_insert = [candle.to_tuple() for candle in candles]
    cursor.executemany(
        "INSERT OR IGNORE INTO price VALUES(?,?,?,?,?,?,?,?)", data_to_insert
    )
    connection.commit()