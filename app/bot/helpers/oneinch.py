import requests
import json
from time import sleep
import os

CHAIN_ID_TO_USE = 8453
FORCE_USE_THIS = True


def parse_response(response_text):
    return json.loads(response_text)

def fetch_token_data(query, chain_id):

    if FORCE_USE_THIS:
        chain_id = CHAIN_ID_TO_USE
        
    apiUrl = f"https://api.1inch.dev/token/v1.2/{chain_id}/search"
    requestOptions = {
        "headers": {
            "Authorization": "Bearer " + os.environ.get('ONEINCH_API_KEY')
        },
        "body": {},
        "params": {
            "query": query,
            "limit": "1"
        }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    response = requests.get(apiUrl, headers=headers, params=params)

    response_text = response.text
    data = parse_response(response_text)
    return data[0]


def generateCallDataForApprove(from_token_address, amount):

        
    apiUrl = f"https://api.1inch.dev/swap/v5.2/{CHAIN_ID_TO_USE}/approve/transaction"
    requestOptions = {
        "headers": {
    "Authorization": "Bearer " + os.environ.get('ONEINCH_API_KEY')
    },
        "body": {},
        "params": {
    "tokenAddress": from_token_address,
    "amount": amount
    }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})


    response = requests.get(apiUrl, headers=headers, params=params)
    
    response_text = response.text

    print(response_text)
    #data = parse_response(response_text)
    return response_text
    
def generateCallDataForSwap(from_address,to_address, amount, wallet_address):
        
    apiUrl = f"https://api.1inch.dev/swap/v5.2/{CHAIN_ID_TO_USE}/swap"
    requestOptions = {
        "headers": {
    "Authorization": "Bearer " + os.environ.get('ONEINCH_API_KEY')
    },
        "body": {},
        "params": {
    "src": to_address,
    "dst": from_address,
    "amount": '1000000000',
    "from": wallet_address,
    "slippage": "1"
    }
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    response = requests.get(apiUrl, headers=headers, params=params)
    
    response_text = response.text
    data = parse_response(response_text)
    return data


def check_token_balances(chain_id,wallet_address):

    if FORCE_USE_THIS:
        chain_id = CHAIN_ID_TO_USE
        
    apiUrl = f"https://api.1inch.dev/balance/v1.2/{chain_id}/balances/{wallet_address}"
    requestOptions = {
        "headers": {
            "Authorization": "Bearer " + os.environ.get('ONEINCH_API_KEY')
        },
        "body": {},
        "params": {}
    }

    # Prepare request components
    headers = requestOptions.get("headers", {})
    body = requestOptions.get("body", {})
    params = requestOptions.get("params", {})

    response = requests.get(apiUrl, headers=headers, params=params)
    
    response_text = response.text
    data = parse_response(response_text)
    
    filtered_data = {k: v for k, v in data.items() if v != '0'}

    sleep(1)

    arr = []
    for token in filtered_data.keys():
        sleep(1)
        a = fetch_token_data(token, chain_id)
        print(a)
        arr.append(a)
        
        
    address_to_token = {token['address']: token for token in arr}

    # Update the balances dictionary with the required fields
    for address, balance in filtered_data.items():
        token = address_to_token.get(address)
        if token:
            filtered_data[address] = {
                'balance': balance,
                'symbol': token['symbol'],
                'name': token['name'],
                'address': token['address'],
                'decimals': token['decimals']
            }

    # Convert the dictionary to an array
    balances_array = list(filtered_data.values())

    
    return balances_array



        
        
def get_prices_for_addresses(addresses, chain_id):
    sleep(1)
    
    if FORCE_USE_THIS:
        chain_id = CHAIN_ID_TO_USE
        
    url = f"https://api.1inch.dev/price/v1.1/{chain_id}/{','.join(addresses)}"

    response = requests.get(url,  headers={'Authorization': "Bearer " + os.environ.get('ONEINCH_API_KEY')})
    if response.status_code == 200:
        prices = response.json()
        return prices

    else:
        return "Failed to fetch token prices."