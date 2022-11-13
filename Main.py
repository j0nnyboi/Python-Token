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


import tkinter
from os.path import exists




class Token(object):

    def __init__(self):
        self.Main_api_endpoint="https://api.mainnet-beta.safecoin.org"
        self.Test_api_endpoint="https://api.testnet.safecoin.org"
        self.Dev_api_endpoint="https://api.devnet.safecoin.org"
        self.api_endpoint = self.Dev_api_endpoint
        self.keypair = ""
        self.top = tkinter.Tk()
        self.wallet_connected = False
        
    def Run(self):
        self.HomePage()
        while True:
            self.top.mainloop()
            

    def HomePage(self):
        wallet_exists = exists('KeyPair.json')
        if(self.wallet_connected == False):
            if(wallet_exists):
                text ="Wallet Connect"
                command = self.WalletConnect
            else:
                text ="Create Wallet"
                command = self.walletNew
            self.wallet = tkinter.Button(self.top, text =text, command = command)
            self.wallet.pack()
        else:
            self.wallet.config(text=self.keypair.public_key)
            
        
        

    def walletNew(self):
        self.keypair = Keypair()
        print([b for b in self.keypair.seed])
        #print(self.keypair.secret_key)
        print(self.keypair.seed)
        print(self.keypair.public_key)
        print(int.from_bytes(self.keypair.seed, "little"))
        with open('KeyPair.json', 'w') as file:
            file.write(str([b for b in self.keypair.seed]))
            
        self.client = Client(self.api_endpoint)
        self.HomePage()

    def WalletConnect(self):
        with open('KeyPair.json', 'r') as KP:
            self.keypairStr = KP.read()
        self.keypairStr.replace("]", '')
        self.keypairStr.replace("[", '')
        print(self.keypairStr)
        print(bytes(self.keypairStr))
        self.keypair = Keypair(bytes(self.keypairStr))
        print(self.keypair.seed)
        self.client = Client(self.api_endpoint)
        self.wallet_connected = True


    def CreateToken(self):
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
        #assert PublicKey(mint_data.mint_authority) == stubbed_sender.public_key
        #assert PublicKey(mint_data.freeze_authority) == freeze_authority.public_key
        return token_client
        
    def CreateAcount(self,token_client):
        token_Account = Token.create_account(
            token_client.pubkey
        )
        return token_Account
        

    def MintToken(self,token_client, amount):
        Token.create_mint(
            token_client.pubkey,
            token_Account,
            amount,
        )

      
Token = Token()
Token.Run()
