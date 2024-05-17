import os
from typing import List

def filter_ticker_list():
    with (
        open("lse.csv", "r") as good_f,
        open("bad_tickers.txt", "r") as bad_f,
        open("lse_clean_alpha.csv", "w") as clean,
    ):
        filtered_tickers = set(good_f.readlines())
        bad_tickers = bad_f.readlines()
        for ticker in bad_tickers:
            if ticker in filtered_tickers:
                filtered_tickers.remove(ticker)
        clean.writelines(filtered_tickers)

def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_tickers(tickers_file:str) -> List[str]:
    path = os.path.join(get_project_root(), tickers_file)
    with open(path, "r") as ticker_file:
        return ticker_file.read().splitlines()