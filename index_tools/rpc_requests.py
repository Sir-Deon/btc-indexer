import os
import requests
from dotenv import load_dotenv # type: ignore

load_dotenv()

# Set up RPC link from getblock
RPC_URL = os.getenv('RPC_URL')

# Make RPC requests
def make_request(method, params = []):
    try:
        # Prepare the request payload
        payload = {
            'method': method,
            'params': params,
            'jsonrpc': '2.0',
            'id': "getblock.io",
        }

        # Make the API request
        response = requests.post(RPC_URL, json=payload)

        # Check the response status code
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()

            # Handle the response data
            if 'result' in data:
                extracted_data = data['result']
                return extracted_data
            elif 'error' in data:
                error = data['error']
                print(f"Error: {error['code']} - {error['message']}")
        else:
            print(f"Request failed with status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print("Error making API request:", e)
        return