# from statsmodels.regression.linear_model import OLS

from pathlib import Path
from typing import Tuple
import pandas as pd
import yfinance as yf
from requests import Session
from requests_cache import CacheMixin, SQLiteCache
from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
from pyrate_limiter import Duration, RequestRate, Limiter
import argparse
import json


class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
    pass

parser = argparse.ArgumentParser(
    prog="yahooCleaner", description="Cleanes data from yfinance"
)
parser.add_argument(
    "-f",
    "--filename",
    default="../data/tickers/lse_big.csv",
    type=str,
    help="Path to csv file with tickers",
)
parser.add_argument("-o", "--output", type=str, help="Path to csv file with tickers")
parser.add_argument(
    "-d", "--debug", action="store_true", help="Path to csv file with tickers"
)

args = parser.parse_args()

# def load_data(path: str | Path, debug: bool = False) -> Tuple[pd.DataFrame, list[str]]:
#     session = CachedLimiterSession(
#         limiter=Limiter(
#             RequestRate(1000, Duration.MINUTE)
#         ),  # max 2 requests per 5 seconds
#         bucket_class=MemoryQueueBucket,
#         backend=SQLiteCache("../data/cache/yfinance.cache"),
#     )
#     tickers_df = pd.read_csv(path)
#     tickers = tickers_df[tickers_df.columns[0]].tolist()
#     if debug:
#         tickers = tickers[0:10]
#     data: pd.DataFrame = yf.download(tickers, period="5y", session=session, repair=True)
#     return data, tickers


def clean_data(price_data: pd.DataFrame, tickers: list[str]) -> list[str]:
    # Fill missing values in the "Close" column with forward-filling
    price_data["Close"] = price_data["Close"].ffill()

    # Count the number of missing values for each ticker
    na_counts = price_data["Close"].isna().sum()

    # Remove tickers with more than 10 missing values
    bad_data_threshold = 10
    bad_tickers = na_counts[na_counts > bad_data_threshold].index.to_list()
    for ticker in bad_tickers:
        tickers.remove(ticker)
        print(f"Ticker {ticker} has {na_counts[ticker]} missing values")
    
    price_data["Close"] = price_data["Close"].bfill()
    # bad_tickers["Close"].
    # # Remove tickers with less than 1277 values
    # # bad_tickers = price_data[(price_data["Close"].isna().sum() > 0) | (len(price_data["Close"]) != 1277)]["Close"].columns.to_list()
    # for ticker in bad_tickers:
    #     tickers.remove(ticker)
    #     print(f"Ticker {ticker} has only {len(price_data['Close'][ticker])}  values")
    # print(price_data.mask(price_data.Close[tickers].isna().sum() > 0)["Close"])
    print(f"Tickers left: {len(tickers)}")
    print(
        f"Tickers with bad data under {bad_data_threshold} "
        f"missing values: {len( bad_tickers)}"
    )
    return tickers


# def save_resulst(
#     price_data: pd.DataFrame, tickers: list, file_path: str | Path, debug: bool = False
# ):
#     pd.DataFrame(tickers).to_csv(file_path, index=False, header=False)
#     data_dir = Path("data")
#     if debug:
#         data_dir = Path("test_data")
#     data_dir.mkdir(parents=True, exist_ok=True)

#     for ticker in tickers:
#         data_f_filled = price_data["Close"][ticker].tolist()
#         path = data_dir / f"{ticker}.json"
#         with open(path, "w") as f:
#             data_to_save = json.dumps(data_f_filled)
#             f.write(data_to_save)


def main():
    ticker_input = Path(args.filename)

    ticker_output = args.output
    if not args.output:
        ticker_output = f"{ticker_input.stem}_clean.csv"

    data, tickers = load_data(ticker_input, args.debug)
    good_tickers = clean_data(data, tickers)
    save_resulst(data, good_tickers, ticker_output, args.debug)


if __name__ == "__main__":
    main()
