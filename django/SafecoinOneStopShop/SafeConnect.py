import argparse
import string
import random
import json
import time
import base58
import base64
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from cryptography.fernet import Fernet
from api.ledamint_api import LedamintAPI
from spl.token.instructions import create_associated_token_account
from safecoin.rpc.commitment import Confirmed
from safecoin.rpc.types import TxOpts
from safecoin.publickey import PublicKey
from safecoin.system_program import TransferParams, transfer
from safecoin.transaction import Transaction
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

class SafeToken(object):
    def __init__(self):
        self.EndPoint = {"Mainnet":"https://api.mainnet-beta.safecoin.org",
                    "Testnet":"https://api.testnet.safecoin.org",
                    "Devnet":"https://api.devnet.safecoin.org"}
        self.api_endpoint = self.EndPoint['Mainnet']
        self.Endpoint_selected = 'Testnet'
        self.keypair = ""
        self.wallet_connected = False

    def ChangeEndpoint(self,endpoint):
        #print("Endpoint Changed: ",endpoint)
        self.client = Client(self.EndPoint[endpoint])
        if(self.client.is_connected()):
            return endpoint
        else:
            return("Connection Error %s" % endpoint)
        

    def WalletConnect(self,keypairStr):
        #with open('KeyPair.json', 'r') as KP:
        #    keypairStr = KP.read()
        print(keypairStr)
        print('here')
        keypairStr = keypairStr.split("[")
        print(keypairStr)
        keypairStr = keypairStr[1].split("]")
        keypairStr = keypairStr[0].split(",")
        keypairStr = keypairStr[0:32]
        print(keypairStr)
        keypairlst = [int(x) for x in keypairStr]
        self.keypair = Keypair(bytes(keypairlst))
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.wallet_connected = True
        return self.keypair

    def walletNew(self):
        self.keypair = Keypair()
        print('newKey')
        print([b for b in self.keypair.seed])
        #print(self.keypair.secret_key)
        print(self.keypair.seed)
        print(self.keypair.public_key)
        #print(int.from_bytes(self.keypair.seed, "little"))
        #with open('KeyPair.json', 'w') as file:
        #    file.write(str([b for b in self.keypair.seed]))
          
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.wallet_connected = True
        return self.keypair

    def deleteKey(self):
        self.wallet_connected = False

    def NewToken(self):
        expected_decimals = 6
        self.token_client = Token.create_mint(
            self.client,
            self.keypair,
            self.keypair.public_key,
            expected_decimals,
            TOKEN_PROGRAM_ID,
            skip_confirmation = True,
            freeze_authority = self.keypair.public_key,
        )
        print(self.token_client.pubkey)
        resp = self.client.get_account_info(self.token_client.pubkey)
        amount = 0
        while resp["result"]["value"] == None:
                print(resp)
                resp = self.client.get_account_info(self.token_client.pubkey)
                time.sleep(1)
                amount += 1
                if(amount > 100):
                    print("Creating a token Failed Please try again \n")
                    return
                    
                
        print(resp)
        assert self.token_client.pubkey
        assert self.token_client.program_id == TOKEN_PROGRAM_ID
        assert self.token_client.payer.public_key == self.keypair.public_key
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)
        Print("Token address = %s \n" % self.token_client.pubkey)
        self.token_PubKey = self.token_client.pubkey
        return self.token_PubKey
        
        

        
