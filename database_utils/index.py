import lmdb
import json

# Open an LMDB environment
env = lmdb.open('../database', max_dbs=10)


def put_data(data, key=None):
    if key is None:
        key_bytes = data["hash"].encode('utf-8')
        data_bytes = json.dumps(data).encode('utf-8')
        # Open a transaction
        with env.begin(write=True) as txn:
            # Put a key-value pair into the database
            txn.put(key_bytes, data_bytes)
        # Close the LMDB environment
        store_key(data["hash"])
        return
    else:
        key_bytes = key.encode('utf-8')
        data_bytes = data.encode('utf-8')
        # Open a transaction
        with env.begin(write=True) as txn:
            # Put a key-value pair into the database
            txn.put(key_bytes, data_bytes)


def get_data(key):
    # Convert the key to bytes
    key_bytes = key.encode('utf-8')
    # Open a transaction
    with env.begin() as txn:
        # Get the value for a key
        data_bytes = txn.get(key_bytes)
        if data_bytes is not None:
            if "hash" in data_bytes.decode('utf-8'):
                data = json.loads(data_bytes.decode('utf-8'))
                return data
            else:
                return data_bytes.decode('utf-8')
        return None


def delete_data(key):
    # Convert the key to bytes
    key_bytes = key.encode('utf-8')

    # Open a transaction
    with env.begin(write=True) as txn:
        # Delete a data
        txn.delete(key_bytes)


def store_key(key):
    file_path = "database/keys.json"
    try:
        with open(file_path, "r") as file:
            # Load the existing JSON data
            existing_data = json.load(file)

        # Append new item to the existing data array
        existing_data.append({"hash": key})

        with open(file_path, "w") as file:
            # Write the updated data to the file
            json.dump(existing_data, file, indent=4)

    except FileNotFoundError:
        # Handle the case when the file does not exist
        with open(file_path, "w") as file:
            json.dump([{"hash": key}], file, indent=4)