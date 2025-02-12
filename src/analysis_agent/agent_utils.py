from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import requests
import time


def get_prices(tickers: list, exchange="CSELK"):
    collection = []
    for ticker in tickers:
        print(ticker)
        tv = TvDatafeed()
        data = tv.get_hist(
            symbol=ticker, exchange=exchange, interval=Interval.in_daily, n_bars=5000
        )
        print(data)
        collection.append(data.pivot(columns="symbol", values="close"))
        time.sleep(7)
    return pd.concat(collection, axis=1).rename(
        columns=lambda x: x.replace("CSELK:", "")
    )


def get_market_caps(tickers: list, currency: str = "LKR"):
    payload = {
        "filter": [{"left": "exchange", "operation": "in_range", "right": ["CSELK"]}],
        "options": {"lang": "en"},
        "symbols": {"query": {"types": []}, "tickers": []},
        "columns": ["name", "market_cap_basic"],
        "sort": {"sortBy": "market_cap_basic", "sortOrder": "desc"},
    }

    url = "https://scanner.tradingview.com/global/scan"
    response = requests.post(url, json=payload)

    caps = dict()
    out = dict()

    current_exchange_rate = get_exchange_rate()

    if response.status_code == 200:
        data_json = response.json()
        stock_data = data_json["data"]
        print(stock_data)
        for stock in stock_data:
            stock_name = stock["d"][0]
            market_cap = stock["d"][1]

            if market_cap is None:
                market_cap = 0
            caps[stock_name] = current_exchange_rate * market_cap

        for ticker in tickers:
            out[ticker] = caps[ticker]

        return out
    else:
        print("Failed to retrieve data")


def get_exchange_rate(currency: str = "LKR"):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        exchange_rate = data["rates"].get(currency, None)

        if exchange_rate:
            return exchange_rate

    return None


