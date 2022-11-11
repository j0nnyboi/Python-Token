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

############################################## Config Wallet and or endpoint ################################################

#api_endpoint="https://api.mainnet-beta.safecoin.org"
#api_endpoint="https://api.testnet.safecoin.org"
api_endpoint="https://api.devnet.safecoin.org"
Wallet_Address = [18,112,244,165,210,145,110,82,195,198,226,197,43,77,241,120,17,201,27,186,65,16,136,114,31,255,109,211,17,238,176,24,143,8,231,110,243,190,132,247,206,213,110,198,197,238,42,232,157,44,223,191,231,236,80,254,179,48,229,226,57,91,159,210]#"Wallet Addresss"
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
    
    walletbytes = bytes(Wallet_Address)
    keypair = Keypair(walletbytes[0:32])
    #print(keypair.seed)
    #print(keypair.public_key)
    cfg = {
        "PRIVATE_KEY": base58.b58encode(keypair.seed).decode("ascii"),
        "PUBLIC_KEY": str(keypair.public_key),
        "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
    }
    #print(cfg)
    api = LedamintAPI(cfg)
    print(api)
    client = Client(api_endpoint)
    print("Connected to %s :" % api_endpoint, client.is_connected())
    if(client.is_connected()):
        
        if(topup == True):
            resp = {}
            while 'result' not in resp:
                resp = client.request_airdrop(keypair.public_key,topupamount * 1000000000)
            txn = resp['result']
            await_full_confirmation(client, txn)
            print(resp)
            print("Topup complete")
        resp = client.get_balance(keypair.public_key)
        print("balance = ", int(resp['result']['value']) / 1000000000)
        resp = client.get_account_info(keypair.public_key)
        print("")
        print("Wallet info ")
        print(resp)
        print("")
        print("Cluster Nodes ")
        print(client.get_cluster_nodes())
        print("")
        print("EPOCH info = ",client.get_epoch_info())
        
    else:
        print("cannot connect to ",api_endpoint)
        
        #resp = api.topup(api_endpoint,Wallet_Address,amount=20)
        #print(resp)

def CreateAtokenAccount():
    mint_public_id = PublicKey("")
    print("mint_public_id = %s",mint_public_id)
    new_wallet = Keypair.generate()
    print("new_wallet = %s",new_wallet)
    transaction = Transaction()
    transaction.add(
        create_associated_token_account(
            new_wallet.public_key, #who is paying for the creation of this token account?
            new_wallet.public_key, #who is the owner of this new token account?
            mint_public_id #what tokens should this token account be able to receive?

        )
    )
    client_devnet = Client(endpoint="https://api.devnet.safecoin.org", commitment=Confirmed)
    client_devnet.request_airdrop(new_wallet.public_key,1000000000)
    client_devnet.get_balance(new_wallet.public_key)
    print(client_devnet.send_transaction(
        transaction, new_wallet, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)))





#WalletConnect(api_endpoint,Wallet_Address,topup,topupamount)
#print("Success! topping up wallet")

"""
    ##
    
    account = Keypair()
    cfg = {"PRIVATE_KEY": base58.b58encode(account.seed).decode("ascii"), "PUBLIC_KEY": Wallet_Address, "DECRYPTION_KEY": Fernet.generate_key().decode("ascii")}
    #api_endpoint = "https://api.devnet.safecoin.org/"*
    Client(api_endpoint).request_airdrop(account.public_key, int(1e10))
    #{'jsonrpc': '2.0', 'result': '4ojKmAAesmKtqJkNLRtEjdgg4CkmowuTAjRSpp3K36UvQQvEXwhirV85E8cvWYAD42c3UyFdCtzydMgWokH2mbM', 'id': 1}
    metaplex_api = LedamintAPI(cfg)
    seller_basis_fees = 0 # value in 10000
    REC = ledamint_api.deploy(api_endpoint, "A"*32, "A"*10, seller_basis_fees)
    print(REC)
    #'{"status": 200, "contract": "7bxe7t1aGdum8o97bkuFeeBTcbARaBn9Gbv5sBd9DZPG", "msg": "Successfully created mint 7bxe7t1aGdum8o97bkuFeeBTcbARaBn9Gbv5sBd9DZPG", "tx": "2qmiWoVi2PNeAjppe2cNbY32zZCJLXMYgdS1zRVFiKJUHE41T5b1WfaZtR2QdFJUXadrqrjbkpwRN5aG2J3KQrQx"}'

    """
    

def test(api_endpoint="https://api.devnet.safecoin.org/"):
    keypair = Keypair()
    cfg = {
        "PRIVATE_KEY": base58.b58encode(keypair.seed).decode("ascii"),
        "PUBLIC_KEY": str(keypair.public_key),
        "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
    }
    api = LedamintAPI(cfg)
    client = Client(api_endpoint)
    resp = {}
    while 'result' not in resp:
        resp = client.request_airdrop(keypair.public_key, int(1e9))
    print("Request Airdrop:", resp)
    txn = resp['result']
    await_full_confirmation(client, txn)
    letters = string.ascii_uppercase
    name = ''.join([random.choice(letters) for i in range(32)])
    symbol = ''.join([random.choice(letters) for i in range(10)])
    print("Name:", name)
    print("Symbol:", symbol)
    # added seller_basis_fee_points
    deploy_response = json.loads(api.deploy(api_endpoint, name, symbol, 0))
    print("Deploy:", deploy_response)
    assert deploy_response["status"] == 200
    contract = deploy_response.get("contract")
    print("contract", contract)
    print(get_metadata(client, contract))
    wallet = json.loads(api.wallet())
    address1 = wallet.get('address')
    encrypted_pk1 = api.cipher.encrypt(bytes(wallet.get('private_key')))
    topup_response = json.loads(api.topup(api_endpoint, address1))
    print(f"Topup {address1}:", topup_response)
    assert topup_response["status"] == 200
    mint_to_response = json.loads(api.mint(api_endpoint, contract, address1, "https://arweave.net/1eH7bZS-6HZH4YOc8T_tGp2Rq25dlhclXJkoa6U55mM/"))
    print("Mint:", mint_to_response)
    await_confirmation(client, mint_to_response['tx'])
    assert mint_to_response["status"] == 200
    print(get_metadata(client, contract))
    wallet2 = json.loads(api.wallet())
    address2 = wallet2.get('address')
    encrypted_pk2 = api.cipher.encrypt(bytes(wallet2.get('private_key')))
    print(client.request_airdrop(api.public_key, int(1e10)))
    topup_response2 = json.loads(api.topup(api_endpoint, address2))
    print(f"Topup {address2}:", topup_response2)
    await_confirmation(client, topup_response2['tx'])
    assert topup_response2["status"] == 200
    send_response = json.loads(api.send(api_endpoint, contract, address1, address2, encrypted_pk1))
    assert send_response["status"] == 200
    await_confirmation(client, send_response['tx'])
    burn_response = json.loads(api.burn(api_endpoint, contract, address2, encrypted_pk2))
    print("Burn:", burn_response)
    await_confirmation(client, burn_response['tx'])
    assert burn_response["status"] == 200
    print("Success!")





"""
print("Now going to mint transfer and burn")
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--network", default=None)
    args = ap.parse_args()
    if args.network == None or args.network == 'devnet':
        test()
    elif args.network == 'devnet':
        test(api_endpoint="https://api.devnet.safecoin.org/")
    elif args.network == 'mainnet':
        test(api_endpoint="https://api.mainnet-beta.safecoin.org/")
    else:
        print("Invalid network argument supplied")

"""
