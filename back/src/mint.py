import logging
import random

from web3.middleware import geth_poa_middleware

from compile import abi
from web3 import Web3


def mint(address, config):
    address = Web3.to_checksum_address(address)
    logging.info(f"mint {address}")

    provider_rpc = config["NFT"]["provider_rpc"]
    web3 = Web3(Web3.HTTPProvider(provider_rpc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account_from = {
        'private_key': config["NFT"]["private_key"],
        'address': config["NFT"]["public_key"],
    }
    contract_address = config["NFT"]["contract_address"]

    contract = web3.eth.contract(address=contract_address, abi=abi)

    metadata, ipfs_hash = get_metadata_and_hash()

    increment_tx = contract.functions.mintNFT(address, f"ipfs://{ipfs_hash}").build_transaction(
        {
            'from': account_from['address'],
            'nonce': web3.eth.get_transaction_count(account_from['address']),
        }
    )

    tx_create = web3.eth.account.sign_transaction(increment_tx, account_from['private_key'])

    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    logging.info(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')
    if "logs" in tx_receipt and len(tx_receipt['logs']) > 1 and "data" in tx_receipt['logs'][1]:
        token_id = int.from_bytes(tx_receipt['logs'][1]['data'], byteorder='big')
        return token_id, metadata


def get_metadata_and_hash():
    probability = random.randint(0, 100)
    if probability < 60:
        filename = "ticket-common.json"
        ipfs_hash = "QmSLqPU23pFyQh2yb4BvQoaja2HLV1NX3hDa1iJcZ1vUn9"
    elif probability < 78:
        filename = "ticket-purple-green.json"
        ipfs_hash = "QmT1EwHPdKYRnWPWGVHm2hopwPEkRN7bVbywjRAksXHhFX"
    elif probability < 96:
        filename = "ticket-red-blue.json"
        ipfs_hash = "QmTY51n9sjzMZ6sB5S6JwhXWH85Bwj9WmFq6dEuZWRyuht"
    else:
        filename = "ticket-gold.json"
        ipfs_hash = "QmXZfKn8fVK4JTvZ25BsJb2Gj9eC6N4t1Jn82MoP7nqEQw"

    with open(f"../data/metadata/{filename}") as file:
        metadata = file.read()

    return metadata, ipfs_hash


