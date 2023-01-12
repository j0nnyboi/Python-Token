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
from coinGeko import getLatestPrice,getLatestPriceArweave,getLatestPriceSafecoin
import requests
import arweave
from arweave.utils import winston_to_ar

class SafeToken(object):
    def __init__(self):
        self.EndPoint = {"Mainnet":"https://api.mainnet-beta.safecoin.org",
                    "Testnet":"https://api.testnet.safecoin.org",
                    "Devnet":"https://api.devnet.safecoin.org"}
        self.api_endpoint = self.EndPoint['Mainnet']
        self.Endpoint_selected = 'Mainnet'
        self.keypair = ""
        self.wallet_connected = False
        self.client = Client(self.EndPoint[self.Endpoint_selected])

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
        print("Token address = %s \n" % self.token_client.pubkey)
        self.token_PubKey = self.token_client.pubkey
        return self.token_PubKey

    def LoadToken(self,TokenPubKey):
        self.token_PubKey = TokenPubKey
        return self.token_PubKey


    def NewTokenACC(self):
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        print(self.token_PubKey)
        
        self.token_Account = self.TokenACCOUNT.create_associated_token_account(self.token_PubKey,skip_confirmation = True)
        print(self.token_Account)
        resp = self.client.get_account_info(self.token_Account)
        amount = 0
        while resp["result"]["value"] == None:
                print(resp)
                resp = self.client.get_account_info(self.token_Account)
                time.sleep(1)
                amount += 1
                if(amount > 100):
                    return
        print(resp)
        print(self.token_Account)
        return (self.token_Account,self.token_PubKey)

    def LoadTokenACC(self,TokenAccPubKey):
        self.token_Account = TokenAccPubKey
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        return (self.token_Account,self.token_PubKey)
        


    def Balance(self):
        if(self.client.is_connected()):
            resp = self.client.get_balance(self.keypair.public_key)
            bal = int(resp['result']['value']) / 1000000000
            #print("balance = ", bal)

            (SafeValue, BWorth) = getLatestPrice(bal)
            #self.SafeVal.configure(text="SafeCoin Price: %.4f USD" % SafeValue)
            #self.walletVal.configure(text="Value: %.4f USD" % BWorth)
            return (bal, SafeValue, BWorth)
            
        else:
            print("Wallet connection ERROR")
            self.client = Client(self.EndPoint[self.Endpoint_selected])
            return 0
        

    def TKNBal(self):
        TokenBall = self.TokenACCOUNT.get_balance(pubkey=self.token_Account)
        #print(TokenBall)
        try:
            bal = int(TokenBall['result']['value']['uiAmount'])
            return bal
        except:
            return 0 
        
    def MintToken(self, amount = 10):
            resp = self.TokenACCOUNT.mint_to(
                dest=self.token_Account,
                mint_authority=self.keypair,
                amount=amount * 1000000,
            )
            print(resp)
            gotTX = self.await_TXN_full_confirmation(self.client,resp['result'])
            return amount


    def await_TXN_full_confirmation(self,client, txn, max_timeout=60):
        if txn is None:
            return False
        elapsed = 0
        gotTX = False
        while elapsed < max_timeout:
            sleep_time = 1
            time.sleep(sleep_time)
            elapsed += sleep_time
            resp = self.client.get_confirmed_transaction(txn)
            print(resp)
            if resp["result"]:
                print(f"Took {elapsed} seconds to confirm transaction {txn}")
                gotTX = True
                return True

        return gotTX

    def airdrop(self):
        resp = {}
        if(self.client.is_connected()):
            while 'result' not in resp:
                resp = self.client.request_airdrop(self.keypair.public_key,1000000000)
            txn = resp['result']
            self.await_TXN_full_confirmation(self.client, txn)
            print(resp)
            print("Topup complete")
            return txn
        else:
            print("not connected to %s"%self.api_endpoint)
            return None


    def Tokenreg(self,TokenName,TokenTicker,TokenDSK,TR_File):


        arweavePrice = getLatestPriceArweave()
        SafecoinPrice = getLatestPriceSafecoin()
        exchangeRate = arweavePrice / SafecoinPrice
        AR_FEE_MULTIPLIER = 20 / 100
        
            
        f_bytes = TR_File.read()
        f_b64 = base64.b64encode(f_bytes).decode("utf8")


        API_URL = "https://arweave.net"
        url = "{}/price/{}".format(API_URL, TR_File.size)

        response = requests.get(url)

        if response.status_code == 200:
             #print("Cost in winston %s " % response.text)
             TokenimgCost = winston_to_ar(response.text)
        else:
            return 'unable to get AR costs'
        #print("TokenCost %s" % TokenimgCost)
        print("SafeAmount exact %s" % (exchangeRate * TokenimgCost))
        Safeamount = ((TokenimgCost * exchangeRate) * 20)
        print("SafeAmount %s" %Safeamount)
        
        #workout amount and send safecoin to es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc so it can be converted to arweave

        txn = Transaction().add(transfer(TransferParams(from_pubkey=self.keypair.public_key, to_pubkey='es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc', lamports=int(Safeamount * 1000000000))))
        snd = self.client.send_transaction(txn, self.keypair)
        print(snd)
        gotTX = self.await_TXN_full_confirmation(self.client,snd['result'])
        if(gotTX):
            pass       
        else:
            return 'Sending safecoin to cover AR conversion failed'
           
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
   
        tokenMetadata = { "name": TokenName,"symbol": TokenTicker,"description": TokenDSK,"image": ""}
        sendDic = {"name": TokenName,
                "symbol": TokenTicker,
                "description": TokenDSK,
                "image": "",
                "updateAuthority": str(self.keypair.public_key),
                "mint": str(self.token_PubKey),
                "mintAuthority": str(self.keypair.public_key),
                "sellerFeeBasisPoints": 0,
                "creators": None,
                "collection": None,
                "uses": None}
        
        payload = json.dumps({"metadata":sendDic, "env":self.EndPoint[self.Endpoint_selected],'transaction':snd['result'],'image':f_b64,'type':TR_File.content_type})
        #print(payload)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post("https://onestopshopBridge.ledamint.io", verify=False,data=payload,headers=headers)
        #response = requests.post("https://onestopshop.ledamint.io",data=payload, headers=headers)

        #print(response.content.decode())
        res = (json.loads(response.text.split('\r\n\r\n')[1])['MetaLink'])
        
        if(res == 'ERROR'):
            return 'Sending safecoin to cover AR conversion failed'
        

        cfg = {
            "PRIVATE_KEY": base58.b58encode(self.keypair.seed).decode("ascii"),
            "PUBLIC_KEY": str(self.keypair.public_key),
            "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
        }
        #print(cfg)
        """
        api = LedamintAPI(cfg)
        result = api.deploy(self.EndPoint[self.Endpoint_selected], TokenName, TokenTicker,0)
        contract_key = json.loads(result).get('contract')
        # conduct a mint, and send to a recipient, e.g. wallet_2
        mint_res = api.mint(self.EndPoint[self.Endpoint_selected], contract_key, self.token_Account, res)
        """
        return res #arwave link    
