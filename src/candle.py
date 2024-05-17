class Candle:
    symbol: str
    _open: float
    high: float
    low: float
    close: float
    volume: float
    date: str

    def __init__(self, symbol: str, date_iso: str, ohlc_data: dict[str, str]):
        self.symbol = symbol
        self._open = float(ohlc_data["1. open"])
        self.high = float(ohlc_data["2. high"])
        self.low = float(ohlc_data["3. low"])
        self.close = float(ohlc_data["4. close"])
        self.volume = float(ohlc_data["5. volume"])
        self.date = date_iso

    def to_tuple(self) -> tuple:
        return (
            self.symbol,
            self.date,
            self.close,
            self._open,
            self.high,
            self.low,
            self.close,
            self.volume,
        )