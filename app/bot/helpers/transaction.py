from web3 import Web3
import os 




infura_url = "https://mainnet.infura.io/v3/"+os.environ.get('INFURA_KEY')  # Replace with your Infura URL

# Connect to the Ethereum network
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if the connection is successful
if web3.isConnected():
    print("Connected to Ethereum network")
else:
    print("Failed to connect")
    
    