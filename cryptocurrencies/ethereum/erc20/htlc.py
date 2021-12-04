#!/usr/bin/env python3

from swap.providers.ethereum.htlc import HTLC
from swap.utils import (
    sha256, get_current_timestamp
)

import json

# Choose network mainnet, ropsten, kovan, rinkeby or testnet
NETWORK: str = "testnet"
# Enable Ethereum HTLC ERC20
ERC20: bool = True
# Ethereum HTLC ERC20 contract address
CONTRACT_ADDRESS: str = "0xf1903D56b808c6480550F4972d250e1B3e968193"
# Secret key hash
SECRET_HASH: str = sha256("Hello Meheret!")
# Ethereum recipient address
RECIPIENT_ADDRESS: str = "0x1954C47a5D75bdDA53578CEe5D549bf84b8c6B94"
# Ethereum sender address
SENDER_ADDRESS: str = "0x69e04fe16c9A6A83076B3c2dc4b4Bc21b5d9A20C"
# Expiration block timestamp
ENDTIME: int = get_current_timestamp(plus=3600)  # 1 hour
# Ethereum ERC20 token address
TOKEN_ADDRESS: str = "0xeaEaC81da5E386E8Ca4De1e64d40a10E468A5b40"

print("=" * 10, "Hash Time Lock Contract (HTLC ERC20) between Sender and Recipient")

# Initialize Ethereum HTLC ERC20
htlc_erc20: HTLC = HTLC(
    contract_address=CONTRACT_ADDRESS, network=NETWORK, erc20=ERC20
)
# Build HTLC ERC20 contract
htlc_erc20.build_htlc(
    secret_hash=SECRET_HASH,
    recipient_address=RECIPIENT_ADDRESS,
    sender_address=SENDER_ADDRESS,
    endtime=ENDTIME,
    token_address=TOKEN_ADDRESS
)

# Print all Ethereum HTLC ERC20 info's
print("HTLC ERC20 Agreements:", json.dumps(htlc_erc20.agreements, indent=4))
print("HTLC ERC20 ABI:", htlc_erc20.abi())
print("HTLC ERC20 Bytecode:", htlc_erc20.bytecode())
print("HTLC ERC20 Bytecode Runtime:", htlc_erc20.bytecode_runtime())
print("HTLC ERC20 OP_Code:", htlc_erc20.opcode())
print("HTLC ERC20 Contract Address:", htlc_erc20.contract_address())
print("HTLC ERC20 Balance:", htlc_erc20.balance(unit="Ether"), "Ether")
print("HTLC ERC20 Balance:", htlc_erc20.erc20_balance(token_address=TOKEN_ADDRESS))

print(json.dumps(dict(
    abi=htlc_erc20.abi(),
    bytecode=htlc_erc20.bytecode(),
    bytecode_runtime=htlc_erc20.bytecode_runtime(),
    contract_address=htlc_erc20.contract_address()
)))

