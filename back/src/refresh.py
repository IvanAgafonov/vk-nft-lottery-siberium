import logging

from web3.middleware import geth_poa_middleware

from compile import abi
from web3 import Web3


def refresh(config, sqlite_client):
    logging.info(f"refresh")

    provider_rpc = config["NFT"]["provider_rpc"]
    web3 = Web3(Web3.HTTPProvider(provider_rpc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    contract_address = config["NFT"]["contract_address"]

    contract = web3.eth.contract(address=contract_address, abi=abi)

    nfts = sqlite_client.execute_select("SELECT * FROM nft;")

    # TODO async with delays
    for nft in nfts:
        owner = contract.functions.ownerOf(nft['tokenId']).call()

        if nft['address'] != owner:
            sqlite_client.execute_update("UPDATE nft SET address = (?) WHERE tokenId = (?)",
                                         (owner, nft['tokenId']))
