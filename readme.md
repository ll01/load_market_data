save example file in the root of the project

example settigns file

```toml
database_name = "market_data.db"
max_workers=4

[[data_sources]]
ticker_file = "data/tickers/lse_tickers.csv"
source = "alphavantage"
interval = "Daily"
requests_a_minute = 4
api_key = "demo"
exchange="LON"


[[data_sources]]
ticker_file = "data/tickers/sp500_tickers.csv"
source = "alphavantage"
interval = "Minute"
requests_a_minute = 4
api_key = "demo"
```

current sources avalible

AlphaVantage

To Do...

add yfinace

add cleaning of data