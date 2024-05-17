"""

downloads data from alphavantage with a rate limiter
"""

from concurrent.futures import ProcessPoolExecutor
from functools import partial
import math
from typing import Any, List, Tuple
from tqdm import tqdm
import os
import tomllib


from alphavantage import AlphaVantage
from datasource import DataSource
from db import open_database
from etl import get_project_root
from interval import Interval
from session import CachedLimiterSession, generate_rate_limiter


def load_data_source(config: dict[str, Any]) -> List[DataSource]:
    data_sources = []
    for data_source in config["data_sources"]:
        if data_source["source"] == "alphavantage":
            exchange = data_source.get("exchange", None)
            data_source = AlphaVantage(
                ticker_file=data_source["ticker_file"],
                interval=Interval[data_source["interval"]],
                api_key=data_source["api_key"],
                requests_a_minute=data_source["requests_a_minute"],
                exchange=exchange,
            )

            data_sources.append(data_source)
    return data_sources


def main():
    settings_path = os.path.join(get_project_root(), "settings.toml")
    if not (os.path.exists(settings_path)):
        print("could not find setting")
    with open(settings_path, "rb") as f:
        config = tomllib.load(f)

        test = config.get("test", False)
        max_workers = config.get("max_workers", 1)
        database_name = config["database_name"]
    data_sources = load_data_source(config)
    open_database(database_name, True)
    
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        for data_source in data_sources:
            tickers = data_source.load_tickers()
            data_source.requests_a_minute = math.ceil(
                data_source.requests_a_minute / max_workers
            )

            list(tqdm(ex.map(data_source.get_data, tickers), total=len(tickers)))


if __name__ == "__main__":
    main()
