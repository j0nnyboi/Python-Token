import argparse
import string
import random
import json
import time
import base58
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from ledamint.metadata import get_metadata
from cryptography.fernet import Fernet
from api.ledamint_api import LedamintAPI

from spl.token.instructions import create_associated_token_account
from safecoin.rpc.commitment import Confirmed
from safecoin.rpc.types import TxOpts
from safecoin.publickey import PublicKey
from safecoin.transaction import Transaction
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

class Token(object):

    def __init__(self):
        self.Main_api_endpoint="https://api.mainnet-beta.safecoin.org"
        self.Test_api_endpoint="https://api.testnet.safecoin.org"
        self.Dev_api_endpoint="https://api.devnet.safecoin.org"
        self.keypair = ""

    def walletNew(self):
        self.keypair = Keypair()
        print(self.keypair.seed)
        print(self.keypair.public_key)
        with open('KeyPair.json', 'w') as file:
            file.write(self.keypair)
        self.client = Client(self.api_endpoint)

    def WalletConnect(self):
        with open('KeyPair.json', 'r') as KP:
            self.keypair = KP.read()
        print(self.keypair)
        walletbytes = bytes(Wallet_Address)
        self.keypair = Keypair(walletbytes)
        self.client = Client(self.api_endpoint)


    def CreateToken(self):
        name = ""
        symbol = ""        

        expected_decimals = 6
        
        token_client = Token.create_mint(
            self.client,
            self.keypair,
            self.keypair.public_key,
            expected_decimals,
            TOKEN_PROGRAM_ID,
            #freeze_authority.public_key,
        )

        assert token_client.pubkey
        assert token_client.program_id == TOKEN_PROGRAM_ID
        assert token_client.payer.public_key == self.keypair.public_key

        resp = self.client.get_account_info(token_client.pubkey)
        assert_valid_response(resp)
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)

        mint_data = layouts.MINT_LAYOUT.parse(decode_byte_string(resp["result"]["value"]["data"][0]))
        assert mint_data.is_initialized
        assert mint_data.decimals == expected_decimals
        assert mint_data.supply == 0
        assert PublicKey(mint_data.mint_authority) == stubbed_sender.public_key
        assert PublicKey(mint_data.freeze_authority) == freeze_authority.public_key
        return token_client
        
        

    def MintToken(self):
        self.TokenClient.create_mint(conn=self.client,mint_authority = self.tokenAccount,decimals=decimals,TOKEN_PROGRAM_ID)

        
