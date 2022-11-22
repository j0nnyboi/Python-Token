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
from safecoin.system_program import TransferParams, transfer
from safecoin.transaction import Transaction
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

import os
import tkinter
from tkinter.scrolledtext import ScrolledText
from os.path import exist

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
        self.top.geometry("900x500")
        self.wallet_connected = False
        self.EndpintVar = tkinter.StringVar(self.top)
        self.EndpintVar.set("Mainnet")
        
        self.AirDropBTN = tkinter.Button(self.top, text ='Airdrop 1 safecoin', command = self.airdrop)
        self.TokenText = ScrolledText(self.top,height = 20, width = 52)
        self.TokenText.place(x=450, y=10)
        self.TokenBTN = tkinter.Button(self.top, text = "Create A Token", command = self.CreateToken)
        #self.TokenBTN = tkinter.Button(self.top, text = "Create A Token", command = self.CreateAcount)
        self.TokenACCBTN = tkinter.Button(self.top, text = "Create A Token Account", command = self.CreateAcount)
        self.MintBtn = tkinter.Button(self.top, text = "MINT", command = self.MintToken)
        self.MintAntLB = tkinter.Label(self.top, text = "Mint Amount:")
        self.AmountBox = tkinter.Text(self.top,height = 1, width = 20)
        self.walletBal = tkinter.Label(self.top, text = "Balance = 0")
        self.TokenLoadBox = tkinter.Text(self.top,height = 1, width = 32)
        self.TokenLoadbtn = tkinter.Button(self.top, text = "Load Token:", command = self.loadToken)
        self.Loadkey = tkinter.Text(self.top,height = 1, width = 32)
        self.loadkeybtn = tkinter.Button(self.top, text = "Load Wallet:", command = self.loadKey)
        self.TokenLoadLB = tkinter.Label(self.top, text = "Load Token :")
        self.TokenLoadAccBox = tkinter.Text(self.top,height = 1, width = 32)
        self.TokenLoadAccbtn = tkinter.Button(self.top, text = "Load Token Account", command = self.loadTokenACC)
        self.TokenLoadlb = tkinter.Label(self.top, text = "Token Account pubkey:")
        self.DeleteKeybtn = tkinter.Button(self.top, text = "Delete key file", command = self.deleteKey)
        self.GetTokenBalbtn = tkinter.Button(self.top, text = "Get Token Balance", command = self.GetTokenBalance)
        self.showWalletbtn = tkinter.Button(self.top, text = "Show wallet import", command = self.Showimort)
        self.loadkeyLB = tkinter.Label(self.top, text = "import wallet:")
        self.DevFeebtn = tkinter.Button(self.top, text = "Dev Tip 1 safecoin", command = self.DevFee)

        
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
                self.DeleteKeybtn.place(x=350, y=50)
                
            else:
                text ="Create New Wallet"
                command = self.walletNew
                
                self.loadkeyLB.place(x=10, y=100)
                self.Loadkey.place(x=100, y=100)
                self.loadkeybtn.place(x=100, y=130)
                self.showWalletbtn.place_forget()
            
            self.wallet = tkinter.Button(self.top, text =text, command = command)
            self.wallet.place(x=10, y=50)
            opt = ["Mainnet", "Testnet", "Devnet"]
            self.Endpoint_Drop = tkinter.OptionMenu(self.top, self.EndpintVar,*(opt),command =self.NetworkChange)    
            self.Endpoint_Drop.place(x=10, y=8)
   
        else:
            self.wallet.config(text=self.keypair.public_key)
            WALLET_BAL = self.WalletBal()
            self.walletBal.place(x=10, y=80)
            self.walletBal.config(text="Ballance = %s" % WALLET_BAL)
            if(self.Endpoint_selected == 'Testnet' or self.Endpoint_selected == 'Devnet'):
                self.AirDropBTN.place(x=10, y=100)
            else:
                self.AirDropBTN.place_forget()
            self.TokenBTN.place(x=10, y=130)
            self.TokenLoadLB.place(x=10, y=170)
            self.TokenLoadBox.place(x=120, y=170)
            self.TokenLoadbtn.place(x=100, y=200)
            self.showWalletbtn.place(x=10,y=400)
            self.DevFeebtn.place(x=10,y=450)
        
    def NetworkChange(self,*args):
        self.Endpoint_selected = self.EndpintVar.get()
        print(self.Endpoint_selected)
        self.EndPoint[self.Endpoint_selected]
        self.EndpintVar.set(self.Endpoint_selected)
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        print(self.EndPoint[self.Endpoint_selected])
        self.HomePage()

        
    def loadKey(self):
        key = self.Loadkey.get("1.0",tkinter.END)
        with open('KeyPair.json', 'w') as file:
            file.write(str(key))

        self.Loadkey.place_forget()
        self.loadkeybtn.place_forget()
        self.loadkeyLB.place_forget()
        self.wallet.place_forget()
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        self.HomePage()
        
    def deleteKey(self):
        os.remove('KeyPair.json')
        self.DeleteKeybtn.place_forget()
        self.Loadkey.place_forget()
        self.loadkeybtn.place_forget()
        self.loadkeyLB.place_forget()
        self.wallet.place_forget()
        self.TokenACCBTN.place_forget()
        self.MintBtn.place_forget()
        self.MintAntLB.place_forget()
        self.AmountBox.place_forget()
        self.walletBal.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.Loadkey.place_forget()
        self.loadkeybtn.place_forget()
        self.TokenLoadLB.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        self.TokenLoadlb.place_forget()
        self.DeleteKeybtn.place_forget()
        self.GetTokenBalbtn.place_forget()
        self.showWalletbtn.place_forget()
        self.loadkeyLB.place_forget()
        self.DevFeebtn.place_forget()
        self.HomePage()

    def Showimort(self):
        secret = [b for b in self.keypair.secret_key]
        print(secret)
        self.TokenText.insert(tkinter.END,"use this string to import into wallet.safecoin.org \n")
        self.TokenText.insert(tkinter.END,"%s \n" % secret)
        self.TokenText.see("end")
        

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
        self.Loadkey.place_forget()
        self.loadkeybtn.place_forget()
        self.loadkeyLB.place_forget()
        self.wallet.place_forget()
        self.HomePage()

    def WalletConnect(self):
        with open('KeyPair.json', 'r') as KP:
            keypairStr = KP.read()
        keypairStr = keypairStr.split("[")
        keypairStr = keypairStr[1].split("]")
        keypairStr = keypairStr[0].split(",")
        keypairStr = keypairStr[0:32]
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
        self.TokenText.see("end")
        self.TokenBTN.place_forget()
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
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
                    self.TokenText.see("end")
                    self.TokenBTN.place(x=200, y=200)
                    self.top.update()
                    return
                    
                
        print(resp)
        assert self.token_client.pubkey
        assert self.token_client.program_id == TOKEN_PROGRAM_ID
        assert self.token_client.payer.public_key == self.keypair.public_key
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)
        self.TokenText.insert(tkinter.END,"Token address = %s \n" % self.token_client.pubkey)
        self.TokenText.see("end")
        self.TokenACCBTN.place(x=10, y=130)
        self.TokenLoadAccBox.place(x=100, y=170)
        self.TokenLoadAccbtn.place(x=100, y=200)
        self.TokenLoadlb.place(x=10, y=170)
        self.token_PubKey = self.token_client.pubkey
        return self.token_client

    def loadToken(self):
        
        token_PubKey = self.TokenLoadBox.get("1.0",tkinter.END)
        self.token_PubKey = token_PubKey.strip('\n')
        print(self.token_PubKey)
        self.TokenText.insert(tkinter.END,"Loaded Token %s \n" % self.token_PubKey)
        self.TokenText.see("end")
        self.TokenACCBTN.place(x=10, y=130)
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenBTN.place_forget()
        self.TokenLoadAccBox.place(x=100, y=170)
        self.TokenLoadAccbtn.place(x=100, y=200)
        self.TokenLoadlb.place(x=10, y=170)

    def loadTokenACC(self):
        token_Account = self.TokenLoadAccBox.get("1.0",tkinter.END)
        self.token_Account = token_Account.strip('\n')
        print(self.token_Account)
        
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)

        self.TokenText.insert(tkinter.END,"Loaded Token Account %s \n" % self.token_Account)
        self.TokenText.see("end")
        self.MintAntLB.place(x=10, y=170)
        self.MintBtn.place(x=100, y=200)
        self.AmountBox.place(x=100, y=170)
        self.AmountBox.insert(tkinter.END,"10")
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenACCBTN.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        self.TokenLoadlb.place_forget()
        self.GetTokenBalbtn.place(x=10, y=130)
        
        
    def CreateAcount(self):
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        print(self.token_PubKey)
        
        self.token_Account = self.TokenACCOUNT.create_account(self.token_PubKey,skip_confirmation = True)
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
                    self.TokenText.see("end")
                    self.top.update()
                    return
        print(resp)
        print(self.token_Account)
        self.MintAntLB.place(x=10, y=270)
        self.MintBtn.place(x=10, y=250)
        self.AmountBox.place(x=100, y=270)
        self.AmountBox.insert(tkinter.END,"10")
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenACCBTN.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        self.TokenLoadlb.place_forget()
        self.TokenText.insert(tkinter.END,"Creating a token Account created %s \n" % self.token_Account)
        self.TokenText.see("end")
        self.top.update()
        return self.token_Account

    def GetTokenBalance(self):
        print(self.token_Account)
        TokenBall = self.TokenACCOUNT.get_balance(pubkey=self.token_Account)
        print(TokenBall)
        self.TokenText.insert(tkinter.END,"Token Ballance = %s \n" % int(TokenBall['result']['value']['uiAmount']))

    def DevFee(self):
        txn = Transaction().add(transfer(TransferParams(from_pubkey=self.keypair.public_key, to_pubkey="JoNVxV8vwBdHqLJ2FT4meLupYKUVVDYr1Pm4DJUp8cZ", lamports=900000200)))
        self.client.send_transaction(txn, self.keypair)
        self.TokenText.insert(tkinter.END,"Thankyou for your support, appreciate all the donations, keeps me making free open source programs")
        self.TokenText.see("end")

    def MintToken(self, amount = 10):
        amount = int(self.AmountBox.get("1.0",tkinter.END))
        print("amount = ",amount)
        self.TokenText.insert(tkinter.END,"Minting %s Tokens\n" % amount)
        self.top.update()
        if(type(amount) == int):
            resp = self.TokenACCOUNT.mint_to(
                dest=self.token_Account,
                mint_authority=self.keypair,
                amount=amount * 1000000,
            )
            print(resp)
            gotTX = self.await_full_confirmation(self.client,resp['result'])
            if(gotTX):
                print(amount, " tokens minted, tx = ",resp['result'])
                self.TokenText.insert(tkinter.END,"Minted %s Tokens\n" % amount)       
            else:
                print("Tokens Failed to mint")
                self.TokenText.insert(tkinter.END,"Tokens Failed to mint please try again\n")
                self.TokenText.see("end")
            self.top.update()
                
        else:
            print("please use just numbers")
            self.TokenText.insert(tkinter.END,"please just use numbers")
            self.TokenText.see("end")
            self.top.update()

    def await_full_confirmation(self,client, txn, max_timeout=60):
        if txn is None:
            return False
        elapsed = 0
        gotTX = False
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
                gotTX = True
                break
        return gotTX

    def airdrop(self):
        resp = {}
        if(self.client.is_connected()):
            self.TokenText.insert(tkinter.END,"Air dropping 1 safe, please wait \n")
            self.TokenText.see("end")
            self.top.update()
            while 'result' not in resp:
                resp = self.client.request_airdrop(self.keypair.public_key,1000000000)
            txn = resp['result']
            self.await_full_confirmation(self.client, txn)
            print(resp)
            print("Topup complete")
            self.TokenText.insert(tkinter.END,"Air drop completed tx = %s \n" % txn)
            self.TokenText.see("end")
            self.HomePage()
        else:
            print("not connected to %s"%self.api_endpoint)
