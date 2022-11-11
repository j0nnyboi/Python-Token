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

############################################## Config Wallet and or endpoint ################################################

api_endpoint="https://api.testnet.safecoin.org"
Wallet_Address = "7bxe7t1aGdum8o97bkuFeeBTcbARaBn9Gbv5sBd9DZPG"#"Wallet Addresss"
topup = False #True if you want to topup
topupamount = 10 # amount to topup

##############################################################################################################################


def await_full_confirmation(client, txn, max_timeout=60):
    if txn is None:
        return
    elapsed = 0
    while elapsed < max_timeout:
        sleep_time = 1
        time.sleep(sleep_time)
        elapsed += sleep_time
        resp = client.get_confirmed_transaction(txn)
        while 'result' not in resp:
            resp = client.get_confirmed_transaction(txn)
        if resp["result"]:
            print(f"Took {elapsed} seconds to confirm transaction {txn}")
            break

def WalletConnect(api_endpoint,Wallet_Address,topup,topupamount):
    
    keypair = Keypair()
    cfg = {
        "PRIVATE_KEY": base58.b58encode(keypair.seed).decode("ascii"),
        "PUBLIC_KEY": str(keypair.public_key),
        "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
    }
    api = LedamintAPI(cfg)
    client = Client(api_endpoint)
    print("Connected to %s :" % api_endpoint, client.is_connected())
    if(client.is_connected()):
        
        if(topup == True):
            resp = {}
            while 'result' not in resp:
                resp = client.request_airdrop(Wallet_Address,topupamount * 1000000000)
            txn = resp['result']
            await_full_confirmation(client, txn)
            print(resp)
            print("Topup complete")

        resp = {}
        name = 'Test'
        symbol = 'mesg'
        print("Name:", name)
        print("Symbol:", symbol)
        # added seller_basis_fee_points
        deploy_response = json.loads(api.deploy(api_endpoint, name, symbol, 0))
        print("Deploy:", deploy_response)
        assert deploy_response["status"] == 200
        contract = deploy_response.get("contract")
        print("contract", contract)
        print(get_metadata(client, contract))
            
        print("Success!")
            
        resp = client.get_balance(Wallet_Address)
        print("balance = ", int(resp['result']['value']) / 1000000000)
        
        
    else:
        print("cannot connect to ",api_endpoint)
        
        #resp = api.topup(api_endpoint,Wallet_Address,amount=20)
        #print(resp)


    



WalletConnect(api_endpoint,Wallet_Address,topup,topupamount)
