
import requests
from datetime import datetime, timedelta
import json
import time
import random

def get_top_cryptocurrencies(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': 'false'
    }
    for i in range(10):  # try 10 times
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # raise exception if invalid response
            data = response.json()
            print(data)
            return [coin['id'] for coin in data]
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep((2 ** i) + random.random())  # exponential backoff

def get_historical_data(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    for i in range(10):  # try 10 times
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # raise exception if invalid response
            data = response.json()
            prices = data['prices']
            return {datetime.fromtimestamp(price[0]/1000).date().isoformat(): price[1] for price in prices}
        except requests.exceptions.RequestException as e:
            print(e)
            time.sleep((2 ** i) + random.random())  # exponential backoff
            
def getHistoricalTokenData():
    top_coins = get_top_cryptocurrencies(limit=10)
    historical_data = {}
    for coin in top_coins:
        print(f"Fetching data for {coin}")
        historical_data[coin] = get_historical_data(coin)
        print(f"Data fetched for {coin}")

    # You can now use historical_data as needed
    print(historical_data)
    
    with open('historical_data_new.json', 'w') as f:
        json.dump(historical_data, f)

    
    
getHistoricalTokenData()