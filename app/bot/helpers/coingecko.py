
import requests
from datetime import datetime, timedelta

def get_top_cryptocurrencies(limit=10):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    data = response.json()
    print(data)
    return [coin['id'] for coin in data]

def get_historical_data(coin_id, days=365):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        'vs_currency': 'usd',
        'days': days
    }
    response = requests.get(url, params=params)
    data = response.json()
    prices = data['prices']
    return {datetime.fromtimestamp(price[0]/1000).date(): price[1] for price in prices}

def getHistoricalTokenData():
    top_coins = get_top_cryptocurrencies(limit=10)
    historical_data = {}
    for coin in top_coins:
        print(f"Fetching data for {coin}")
        historical_data[coin] = get_historical_data(coin)
        print(f"Data fetched for {coin}")

    # You can now use historical_data as needed
    print(historical_data)