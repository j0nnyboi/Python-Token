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
        self.Endpoint_selected = 'Mainnet'
        self.keypair = ""
        self.wallet_connected = False

    def WalletConnect(self,keypairStr):
        #with open('KeyPair.json', 'r') as KP:
        #    keypairStr = KP.read()
        keypairStr = keypairStr.split("[")
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
        print([b for b in self.keypair.seed])
        #print(self.keypair.secret_key)
        print(self.keypair.seed)
        print(self.keypair.public_key)
        print(int.from_bytes(self.keypair.seed, "little"))
        #with open('KeyPair.json', 'w') as file:
        #    file.write(str([b for b in self.keypair.seed]))
          
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.wallet_connected = True
        return self.keypair

    def deleteKey(self):
        self.wallet_connected = False
        

        
