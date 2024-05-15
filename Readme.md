# Bitcoin transaction indexer

This is my first bitcoin transaction indexer 

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Sir-Deon/btc-indexer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd project-name
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   conda create bitcoin_indexer
   ```

4. Activate the virtual environment:

    ```bash
   conda activate bitcoin_indexer
   ```

5. Install the project dependencies from the requirements.txt file:

   ```bash
   pip install -r requirements.txt
   ```

   This command will install all the required dependencies listed in the requirements.txt file.

6. Run the project:

   ```bash
   python main.py
   ```

## Resources

I made use of the following resources

1. I used RPC API from https://getblock.io
2. I also made use of a key value pair dm called lmdb, because i had issues installing rocksdb

