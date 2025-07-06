from tvDatafeed import TvDatafeed, Interval
import pandas as pd
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


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



def get_company_overview_metrics(ticker):
    """Fetch financial overview data from TradingView for a given ticker and return as a dictionary."""
    
    # Initialize Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the TradingView financials page
        url = f"https://www.tradingview.com/symbols/CSELK-{ticker}/financials-overview/"
        driver.get(url)
        time.sleep(5)
        # Find all div elements with class 'item-D38HaCsG'
        div_elements = driver.find_elements(By.CLASS_NAME, 'item-D38HaCsG')

        # Extract financial data into a dictionary
        financial_data = {}
        for div in div_elements:
            try:
                # Find the title span
                title_span = div.find_element(By.CSS_SELECTOR, '.title-D38HaCsG.apply-overflow-tooltip')
                title_text = title_span.text.strip()

                # Find the data span
                data_span = div.find_element(By.CLASS_NAME, 'data-D38HaCsG')
                data_text = data_span.text.replace('\u202a', '').replace('\u202c', '').replace('\u202f', '').strip()

                # Store data in dictionary
                financial_data[title_text] = data_text

            except Exception as e:
                print(f"Error extracting data from div: {e}")

        return financial_data

    finally:
        # Close the browser after extraction
        driver.quit()






# data = get_company_overview_metrics("HNB.N0000")
# print(data)