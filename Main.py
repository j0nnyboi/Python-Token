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




class Safecoin_Token(object):

    def __init__(self):

        self.EndPoint = {"Mainnet":"https://api.mainnet-beta.safecoin.org",
                    "Testnet":"https://api.testnet.safecoin.org",
                    "Devnet":"https://api.devnet.safecoin.org"}
        self.api_endpoint = self.EndPoint['Mainnet']
        self.Endpoint_selected = 'Mainnet'
        print(self.api_endpoint)
        self
        self.keypair = ""
        self.top = tkinter.Tk()
        self.top.geometry("800x500")
        self.wallet_connected = False
        self.EndpintVar = tkinter.StringVar(self.top)
        self.EndpintVar.set("Mainnet")
        
        self.AirDropBTN = tkinter.Button(self.top, text ='Airdrop 1 safecoin', command = self.airdrop)
        self.TokenText = tkinter.Text(self.top,height = 20, width = 52)
        self.TokenText.place(x=300, y=10)
        self.TokenBTN = tkinter.Button(self.top, text = "Create A Token", command = self.CreateToken)
        #self.TokenBTN = tkinter.Button(self.top, text = "Create A Token", command = self.CreateAcount)
        self.TokenACCBTN = tkinter.Button(self.top, text = "Create A Token Account", command = self.CreateAcount)
        self.MintBtn = tkinter.Button(self.top, text = "MINT", command = self.MintToken)
        
    def Run(self):
        self.HomePage()
        while True:
            self.top.mainloop()
            
    def WalletBal(self):
        if(self.client.is_connected()):
            resp = self.client.get_balance(self.keypair.public_key)
            bal = int(resp['result']['value']) / 1000000000
            print("balance = ", bal)
            return bal
        else:
            print("Wallet connection ERROR")
            self.client = Client(self.EndPoint[self.Endpoint_selected])
            return 0
    
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
            self.wallet.place(x=10, y=10)
            self.walletBal = tkinter.Label(self.top, text = "Ballance = 0")
            self.walletBal.place(x=10, y=50)
            opt = ["Mainnet", "Testnet", "Devnet"]
            self.Endpoint_Drop = tkinter.OptionMenu(self.top, self.EndpintVar,*(opt),command =self.NetworkChange)    
            self.Endpoint_Drop.place(x=10, y=100)
            
            
        else:
            self.wallet.config(text=self.keypair.public_key)
            WALLET_BAL = self.WalletBal()
            self.walletBal.config(text="Ballance = %s" % WALLET_BAL)
            if(self.Endpoint_selected == 'Testnet' or self.Endpoint_selected == 'Devnet'):
                self.AirDropBTN.place(x=100, y=50)
            else:
                self.AirDropBTN.place_forget()
            self.TokenBTN.place(x=200, y=200)
        
    def NetworkChange(self,*args):
        self.Endpoint_selected = self.EndpintVar.get()
        print(self.Endpoint_selected)
        self.EndPoint[self.Endpoint_selected]
        self.EndpintVar.set(self.Endpoint_selected)
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        print(self.EndPoint[self.Endpoint_selected])
        self.HomePage()
        

    def walletNew(self):
        self.keypair = Keypair()
        print([b for b in self.keypair.seed])
        #print(self.keypair.secret_key)
        print(self.keypair.seed)
        print(self.keypair.public_key)
        print(int.from_bytes(self.keypair.seed, "little"))
        with open('KeyPair.json', 'w') as file:
            file.write(str([b for b in self.keypair.seed]))
            
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.HomePage()

    def WalletConnect(self):
        with open('KeyPair.json', 'r') as KP:
            keypairStr = KP.read()
        keypairStr = keypairStr.split("[")
        keypairStr = keypairStr[1].split("]")
        keypairStr = keypairStr[0].split(",")
        print(keypairStr)
        keypairlst = [int(x) for x in keypairStr]
        
        #print(self.keypairStr)
        #print(bytearray(self.keypairStr))
        self.keypair = Keypair(bytes(keypairlst))
        print(self.keypair.seed)
        print(self.keypair.public_key)
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.wallet_connected = True
        self.HomePage()


    def CreateToken(self):
        self.TokenText.insert(tkinter.END,"Creating a token and waiting for confirmation \n")
        self.TokenBTN.place_forget()
        self.top.update()
        expected_decimals = 6
        self.token_client = Token.create_mint(
            self.client,
            self.keypair,
            self.keypair.public_key,
            expected_decimals,
            TOKEN_PROGRAM_ID,
            skip_confirmation = True,
            #freeze_authority.public_key,
        )
        print(self.token_client.pubkey)
        resp = self.client.get_account_info(self.token_client.pubkey)
        amount = 0
        while resp["result"]["value"] == None:
                print(resp)
                resp = self.client.get_account_info(self.token_client.pubkey)
                self.top.update()
                time.sleep(1)
                amount += 1
                if(amount > 100):
                    self.TokenText.insert(tkinter.END,"Creating a token Failed Please try again \n")
                    self.TokenBTN.place(x=200, y=200)
                    self.top.update()
                    return
                    
                
        print(resp)
        assert self.token_client.pubkey
        assert self.token_client.program_id == TOKEN_PROGRAM_ID
        assert self.token_client.payer.public_key == self.keypair.public_key
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)
        self.TokenText.insert(tkinter.END,"Token address = %s \n" % self.token_client.pubkey)
        self.TokenACCBTN.place(x=200, y=200)
        return self.token_client
        
    def CreateAcount(self):
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_client.pubkey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        print(self.token_client.pubkey)
        
        self.token_Account = self.TokenACCOUNT.create_account(self.token_client.pubkey,skip_confirmation = True)
        print(self.token_Account)
        resp = self.client.get_account_info(self.token_Account)
        amount = 0
        while resp["result"]["value"] == None:
                print(resp)
                resp = self.client.get_account_info(self.token_Account)
                self.top.update()
                time.sleep(1)
                amount += 1
                if(amount > 100):
                    self.TokenText.insert(tkinter.END,"Creating a token Account Failed Please try again \n")
                    self.top.update()
                    return
        print(resp)
        print(self.token_Account)
        self.MintBtn.place(x=200, y=250)
        return self.token_Account
        

    def MintToken(self, amount = 10):
        self.TokenACCOUNT.mint_to(
            dest=self.token_client.pubkey,
            mint_authority=self.keypair,
            amount=amount,
        )

    def await_full_confirmation(self,client, txn, max_timeout=60):
        if txn is None:
            return
        elapsed = 0
        while elapsed < max_timeout:
            sleep_time = 1
            time.sleep(sleep_time)
            elapsed += sleep_time
            resp = self.client.get_confirmed_transaction(txn)
            while 'result' not in resp:
                print(resp)
                resp = self.client.get_confirmed_transaction(txn)
            if resp["result"]:
                print(f"Took {elapsed} seconds to confirm transaction {txn}")
                break

    def airdrop(self):
        resp = {}
        if(self.client.is_connected()):
            while 'result' not in resp:
                resp = self.client.request_airdrop(self.keypair.public_key,1000000000)
            txn = resp['result']
            self.await_full_confirmation(self.client, txn)
            print(resp)
            print("Topup complete")
            self.HomePage()
        else:
            print("not connected to %s"%self.api_endpoint)

      
Safe_Token = Safecoin_Token()
Safe_Token.Run()
