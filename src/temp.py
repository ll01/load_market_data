# """
# Download data from yfinance
# """

# import pandas as pd
# import yfinance as yf
# from requests import Session
# from requests_cache import CacheMixin, SQLiteCache
# from requests_ratelimiter import LimiterMixin, MemoryQueueBucket
# from pyrate_limiter import Duration, RequestRate, Limiter
# class CachedLimiterSession(CacheMixin, LimiterMixin, Session):
#     pass

# session = CachedLimiterSession(
#     limiter=Limiter(RequestRate(2, Duration.SECOND*5)),  # max 2 requests per 5 seconds
#     bucket_class=MemoryQueueBucket,
#     backend=SQLiteCache("../data/cache/yfinance.cache"),
# )
# tickers_df = pd.read_csv("../data/tickers/lse_big.csv")
# tickers = tickers_df[tickers_df.columns[0]].tolist()
# data: pd.DataFrame = yf.download(tickers, period="5y", session=session, repair=True)


# for ticker in tickers.copy():
#     data_f_filled = data["Close"][ticker].ffill()
#     na_count = data_f_filled.isna().sum()
#     if na_count > 0:
#         tickers.remove(ticker)
#         print(f"Ticker {ticker} has {na_count} missing values")

# print(f"Tickers left: {len(tickers)}")
# pd.DataFrame(tickers).to_csv("lse.csv", index=False, header=False)




from concurrent.futures import ProcessPoolExecutor
import multiprocessing


def running_proxy(mval):
    # consider lock if you need
    print(f"Current value: {mval.value}")
    return mval.value

def start_executor():
    with multiprocessing.Manager() as manager:
        executor = ProcessPoolExecutor(max_workers=5)
        mval = manager.Value('b', 1)
        futures = [executor.submit(running_proxy, mval) for _ in range(5)]
        results = [x.result() for x in futures]
        executor.shutdown()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    start_executor()