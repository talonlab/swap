#!/usr/bin/env python3

import requests
import json

from shuttle.providers.bitcoin.utils import is_address
from shuttle.providers.config import bitcoin


# Request headers
headers = dict()
headers.setdefault("Content-Type", "application/json")
# Bitcoin configuration
bitcoin = bitcoin()


# Get balance by address
def get_balance(address, network="testnet", timeout=5):
    assert is_address(address), "Invalid address!"
    url = str(bitcoin[network]["blockcypher"]) + ("/addrs/%s/balance" % address)
    return requests.get(url=url, headers=headers, timeout=timeout).json()["balance"]


# Get unspent transaction by address
def get_unspent_transactions(address, network="testnet", include_script=True, limit=50, timeout=15):
    assert is_address(address), "Invalid address!"
    _include_script = "true" if include_script else "false"
    parameter = dict(limit=limit, unspentOnly="true",
                     includeScript=_include_script, token=bitcoin[network]["blockcypher"]["token"])
    url = bitcoin[network]["blockcypher"]["url"] + ("/addrs/%s" % address)
    response = requests.get(url=url, params=parameter, headers=headers, timeout=timeout).json()
    return response["txrefs"] if "txrefs" in response else []


# Getting decode transaction by transaction raw
def decoded_transaction_raw(transaction_raw, network="testnet", timeout=5):
    if isinstance(transaction_raw, str):
        parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
        tx = json.dumps(dict(tx=transaction_raw))
        return requests.post(url=bitcoin[network]["blockcypher"]["url"] + "/txs/decode",
                             data=tx, params=parameter, headers=headers, timeout=timeout).json()
    raise TypeError("Transaction raw must be string format!")


# Getting push transaction by transaction raw
def push_transaction_raw(transaction_raw, network="testnet", timeout=5):
    if isinstance(transaction_raw, str):
        parameter = dict(token=bitcoin[network]["blockcypher"]["token"])
        tx = json.dumps(dict(tx=transaction_raw))
        return requests.post(url=bitcoin[network]["blockcypher"]["url"] + "/txs/push",
                             data=tx, params=parameter, headers=headers, timeout=timeout).json()
    raise TypeError("Transaction raw must be string format!")
