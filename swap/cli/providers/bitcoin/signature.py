#!/usr/bin/env python
# coding=utf-8

from base64 import b64decode

import json
import sys

from ....cli import click
from ....providers.bitcoin.solver import (
    FundSolver, ClaimSolver, RefundSolver
)
from ....providers.bitcoin.signature import (
    FundSignature, ClaimSignature, RefundSignature
)
from ....providers.bitcoin.utils import is_transaction_raw
from ....providers.config import bitcoin
from ....utils.exceptions import TransactionRawError
from ....utils import clean_transaction_raw

# Bitcoin config
config = bitcoin()


@click.command("sign", options_metavar="[OPTIONS]",
               short_help="Select Bitcoin transaction raw signer.")
@click.option("-rx", "--root-xprivate", type=str, required=True, help="Set Bitcoin root xprivate key.")
@click.option("-r", "--raw", type=str, required=True, help="Set Bitcoin unsigned transaction raw.")
@click.option("-b", "--bytecode", type=str, default=None,
              help="Set Bitcoin witness HTLC bytecode.  [default: None]", show_default=True)
@click.option("-s", "--secret-key", type=str, default=None,
              help="Set secret key.  [default: None]", show_default=True)
@click.option("-sq", "--sequence", type=int, default=config["sequence"],
              help="Set Bitcoin sequence/expiration block.", show_default=True)
@click.option("-ac", "--account", type=int, default=1,
              help="Set Bitcoin derivation from account.", show_default=True)
@click.option("-c", "--change", type=bool, default=False,
              help="Set Bitcoin derivation from change.", show_default=True)
@click.option("-ad", "--address", type=int, default=1,
              help="Set Bitcoin derivation from address.", show_default=True)
@click.option("-p", "--path", type=str, default=None,
              help="Set Bitcoin derivation from path.  [default: None]", show_default=True)
@click.option("-v", "--version", type=int, default=config["version"],
              help="Set Bitcoin transaction version.", show_default=True)
def sign(root_xprivate, raw, bytecode, secret_key, sequence, account, change, address, path, version):

    try:
        if not is_transaction_raw(transaction_raw=raw):
            raise TransactionRawError("Invalid Bitcoin unsigned transaction raw.")

        transaction_raw = clean_transaction_raw(raw)
        decoded_transaction_raw = b64decode(transaction_raw.encode())
        loaded_transaction_raw = json.loads(decoded_transaction_raw.decode())
        
        if loaded_transaction_raw["type"] == "bitcoin_fund_unsigned":
            # Fund HTLC solver
            fund_solver = FundSolver(
                root_xprivate_key=root_xprivate,
                account=account, change=change, address=address,
                path=path
            )
            # Fund signature
            fund_signature = FundSignature(
                network=loaded_transaction_raw["network"], version=version
            )
            fund_signature.sign(
                transaction_raw=raw, solver=fund_solver
            )
            click.echo(fund_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "bitcoin_claim_unsigned":
            if secret_key is None:
                click.echo(click.style("Error: {}").format(
                    "Secret key is required for claim, use -s or --secret_key \"Hello Meheret!\""
                ), err=True)
                sys.exit()
            if bytecode is None:
                click.echo(click.style("Error: {}").format(
                    "Witness bytecode is required for claim, use -b or --bytecode \"016...\""
                ), err=True)
                sys.exit()

            # Claim HTLC solver
            claim_solver = ClaimSolver(
                root_xprivate_key=root_xprivate, secret_key=secret_key, bytecode=bytecode,
                account=account, change=change, address=address,
                path=path
            )
            # Claim signature
            claim_signature = ClaimSignature(
                network=loaded_transaction_raw["network"], version=version
            )
            claim_signature.sign(
                transaction_raw=raw, solver=claim_solver
            )
            click.echo(claim_signature.transaction_raw())

        elif loaded_transaction_raw["type"] == "bitcoin_refund_unsigned":
            if bytecode is None:
                click.echo(click.style("Error: {}").format(
                    "Witness bytecode is required for refund, use -b or --bytecode \"016...\""
                ), err=True)
                sys.exit()

            # Refunding HTLC solver
            refund_solver = RefundSolver(
                root_xprivate_key=root_xprivate, bytecode=bytecode, sequence=sequence,
                account=account, change=change, address=address,
                path=path
            )
            # Refund signature
            refund_signature = RefundSignature(
                network=loaded_transaction_raw["network"], version=version
            )
            refund_signature.sign(
                transaction_raw=raw, solver=refund_solver
            )
            click.echo(refund_signature.transaction_raw())
        else:
            click.echo(click.style("Error: {}")
                       .format("Unknown Bitcoin unsigned transaction raw type."), err=True)
            sys.exit()
    except Exception as exception:
        click.echo(click.style("Error: {}").format(str(exception)), err=True)
        sys.exit()
