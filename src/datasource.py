from abc import ABC, abstractmethod
from multiprocessing.managers import ValueProxy
from typing import List
from etl import load_tickers
from session import CachedLimiterSession, generate_rate_limiter
from interval import Interval
from candle import Candle
import uuid


class DataSource(ABC):
    def __init__(
        self,
        name: str,
        ticker_file: str,
        interval: Interval,
        requests_a_minute: int
    ) -> None:
        self.name = name
        self.interval = interval
        self.ticker_file = ticker_file
        self.requests_a_minute = requests_a_minute
        self.session = None

    def load_tickers(self) -> List[str]:
        return load_tickers(self.ticker_file)

    @abstractmethod
    def get_data(self, ticker: str) -> List[Candle]:
        self.session = generate_rate_limiter(self.requests_a_minute)