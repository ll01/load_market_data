from datetime import datetime
from multiprocessing.managers import ValueProxy
from typing import List

import orjson

from datasource import DataSource
from interval import Interval
from candle import Candle
from session import CachedLimiterSession
# from session import CachedLimiterSession, SessionManager

class AlphaVantage(DataSource):
    def __init__(
        self,
        ticker_file: str,
        interval: Interval,
        api_key: str,
        requests_a_minute: int,
        exchange=None,
    ):
        super().__init__("alphavantage", ticker_file, interval, requests_a_minute)
        self.api_key = api_key
        self.exchange = exchange

    def get_data(
        self, ticker: str
    ) -> List[Candle]:
        super().get_data(ticker)
        candles = []
        base_url = "https://www.alphavantage.co/query?"
        if self.interval == Interval.Daily:
            function = "TIME_SERIES_DAILY"
            data_label = "Time Series (Daily)"
            date_format = "%Y-%m-%d"
            if self.exchange:
                ticker = f"{ticker}.{self.exchange}"

        elif self.interval == Interval.Minute:
            function = "TIME_SERIES_INTRADAY"
            base_url += "&interval=1min&extended_hours=false&"
            data_label = "Time Series (1min)"
            date_format = "%Y-%m-%d %H:%M:%S"

        url = (
            f"{base_url}function={function}&symbol={ticker}&apikey={self.api_key}"
            f"&outputsize=full"
        )
        if self.session is None:
            return []
        result = self.session.get(url)
        if result.text and "Error Message" not in result.text:
            content = orjson.loads(result.text)
            price_data: dict[str, dict[str, str]] = content.get(data_label)
            if price_data:
                for dateTimeString, ohlc_data in price_data.items():
                    formated_datetime = datetime.strptime(
                        dateTimeString, date_format
                    ).isoformat()
                    candles.append(Candle(ticker, formated_datetime, ohlc_data))
        return candles
