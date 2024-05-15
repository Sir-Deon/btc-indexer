import os
import time
import requests # type: ignore
from dotenv import load_dotenv # type: ignore
from index_tools.utils import *
from database_utils.index import *
from database_utils.schema import transaction

load_dotenv()


WEBHOOK_URL = os.getenv('WEBHOOK_URL')
MONITORED_ADDRESS = os.getenv('MONITORED_ADDRESS')

print(WEBHOOK_URL)
put_data(MONITORED_ADDRESS, "monitored_address")

# This function is responsible for periodically getting new blocks
def continualy_get_blocks():
    # Retrieve new blocks
    print("Retrieving blocks...")
    latest_block_count = get_block_count()

    while True:
        current_block_count = get_block_count()
        print(current_block_count)
        if current_block_count > latest_block_count:
            latest_block_count = current_block_count

            latest_block_hash = get_block_hash(current_block_count)
            latest_block_data = get_block_data(latest_block_hash)
            print(len(latest_block_data["tx"]))

        time.sleep(1)  # Wait for 1 second before checking for new blocks


# This function periodically gets transaction from mempool
def continualy_get_mempool():
    # Retrieve mempool data
    print("Retrieving mempool data...")
    latest_transaction_hash = get_mempool_data()[-1]
    while True:
        current_transaction_hash =  get_mempool_data()[-1]
        if current_transaction_hash != latest_transaction_hash:
            latest_transaction_hash = current_transaction_hash

            transaction_details = get_transaction_details(latest_transaction_hash)
   
            # Puting the transaction details into the transaction
            transaction["hash"] = transaction_details["hash"]
            transaction["sender_address"] = get_sender_address(transaction_details["txid"])
            transaction["receiver_address"] = transaction_details["vout"][0]["scriptPubKey"]["address"]
            transaction["amount"] =  transaction_details["vout"][0]["value"]
            transaction["weight"] =  transaction_details["weight"]
            transaction["version"] =  transaction_details["version"]
            # Store in the db
            put_data(transaction)
            monitor_address = get_data("monitored_address")
            if monitor_address == transaction["receiver_address"] or monitor_address == transaction["sender_address"] :
                notification = {
                    "hash": transaction["hash"],
                    "amount":  transaction["amount"],
                    "address": monitor_address,
                    "type": "received" if monitor_address == transaction["receiver_address"]  else "sent"
                }
                send_notification(notification)

        time.sleep(1)

continualy_get_mempool()


def send_notification(data):
    # Send a POST request to the webhook endpoint
    response = requests.post(WEBHOOK_URL, json=data)

    # Check the response status code
    if response.status_code == 200:
        print("Webhook request successful!")
    else:
        print(f"Webhook request failed with status code: {response.status_code}")
