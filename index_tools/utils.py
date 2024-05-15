from index_tools.rpc_requests import *
import requests

# Continuously monitor the mempool for new transactions
def get_mempool_data():
    result = make_request('getrawmempool')
    return result
   


# Get the block count
def get_block_count():
     # Make request
    count = make_request('getblockcount')
    return count
   
    
# Get the block hash
def get_block_hash(count):
    hash = make_request('getblockhash', [count])
    return hash


def get_block_data(hash):
    data = make_request('getblock', [hash])
    return data


def get_transaction_details(hash):
    data = make_request('getrawtransaction', [hash, True])
    return data


def get_sender_address(transaction_id):
    base_url = "https://blockstream.info/testnet/api"
    transaction_url = f"{base_url}/tx/{transaction_id}"
    try:
        response = requests.get(transaction_url)
        transaction_data = response.json()
        vin_txid = transaction_data["vin"][0]["txid"]
        vin_vout = transaction_data["vin"][0]["vout"]

        sender_tx_url = f"{base_url}/tx/{vin_txid}"
        response = requests.get(sender_tx_url)
        sender_tx_data = response.json()

        sender_address = sender_tx_data["vout"][vin_vout]["scriptpubkey_address"]

        return sender_address
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return
