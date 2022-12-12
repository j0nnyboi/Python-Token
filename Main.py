import argparse
import string
import random
import json
import time
import base58
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from ledamint.metadata import get_metadata, get_metadata_account
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
from tkinter import filedialog

from time import gmtime, strftime,sleep
import os
import tkinter
from tkinter.scrolledtext import ScrolledText
from os.path import exists
import threading
import arweave
import customtkinter
from time import gmtime, strftime
import json
import ValidatorMonitor
from coinGeko import getLatestPrice



customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green") 

class Safecoin_Token(object):

    def __init__(self):

        self.EndPoint = {"Mainnet":"https://api.mainnet-beta.safecoin.org",
                    "Testnet":"https://api.testnet.safecoin.org",
                         
                    "Devnet":"https://api.devnet.safecoin.org"}
        self.api_endpoint = self.EndPoint['Mainnet']
        self.Endpoint_selected = 'Mainnet'
        print(self.api_endpoint)
        self.keypair = ""
        self.top = customtkinter.CTk()
        self.top.title("SafeCoin one stop shop")
        self.top.geometry("900x500")
        self.wallet_connected = False
        self.EndpintVar = tkinter.StringVar(self.top)
        self.EndpintVar.set("Mainnet")
        
        self.AirDropBTN = customtkinter.CTkButton(self.top, text ='Airdrop 1 safecoin', command = self.airdrop)
        self.TokenText = customtkinter.CTkTextbox(self.top,height = 400, width = 380)
        self.TokenText.place(x=500, y=10)
        self.TokenBTN = customtkinter.CTkButton(self.top, text = "Create A Token", command = self.CreateToken)
        #self.TokenBTN = customtkinter.CTkButton(self.top, text = "Create A Token", command = self.CreateAcount)
        self.TokenACCBTN = customtkinter.CTkButton(self.top, text = "Create A Token Account", command = self.CreateAcount)
        self.MintBtn = customtkinter.CTkButton(self.top, text = "MINT", command = self.MintToken)
        self.MintAntLB = customtkinter.CTkLabel(self.top, text = "Mint Amount:",width=30, height=25)
        self.AmountBox = customtkinter.CTkEntry(self.top,height = 25, width = 100)
        self.walletBal = customtkinter.CTkLabel(self.top, text = "Balance = 0")
        self.walletVal = customtkinter.CTkLabel(self.top, text = "Value = *")
        self.SafeVal = customtkinter.CTkLabel(self.top, text = "SafeCoin Price: *")
        self.TokenLoadBox = customtkinter.CTkEntry(self.top,height = 25, width = 300)
        self.TokenLoadbtn = customtkinter.CTkButton(self.top, text = "Load Token:", command = self.loadToken)
        self.Loadkey = customtkinter.CTkEntry(self.top,height = 25, width = 300)
        self.loadkeybtn = customtkinter.CTkButton(self.top, text = "Load Wallet:", command = self.loadKey)
        self.TokenLoadLB = customtkinter.CTkLabel(self.top, text = "Load Token :",width=30, height=25)
        self.TokenLoadAccBox = customtkinter.CTkEntry(self.top,height = 25, width = 300)
        self.TokenLoadAccbtn = customtkinter.CTkButton(self.top, text = "Load Token Account", command = self.loadTokenACC)
        self.TokenLoadlb = customtkinter.CTkLabel(self.top, text = "Token Account pubkey:",width=30, height=25)
        self.DeleteKeybtn = customtkinter.CTkButton(self.top, text = "Delete key file", command = self.deleteKey)
        self.GetTokenBalbtn = customtkinter.CTkButton(self.top, text = "Get Token Balance", command = self.GetTokenBalance)
        self.showWalletbtn = customtkinter.CTkButton(self.top, text = "Show wallet import", command = self.Showimort)
        self.loadkeyLB = customtkinter.CTkLabel(self.top, text = "import wallet:",width=30, height=25)
        self.DevFeebtn = customtkinter.CTkButton(self.top, text = "Dev Tip 1 safecoin", command = self.DevFee)
        self.HomePagebtn = customtkinter.CTkButton(self.top, text = "Home", command = self.ClearHomepage)
        self.TKNorNFT = 0
        self.OwnMint=True
        self.TKNbtn = customtkinter.CTkButton(self.top, text = "TOKEN", command = lambda:self.TKN_NFT(1))
        self.NFTbtn = customtkinter.CTkButton(self.top, text = "NFT", command = lambda:self.TKN_NFT(2))
        self.Homebtn = customtkinter.CTkButton(self.top, text = "Reset", command = lambda:self.TKN_NFT(0))
        self.NFTSinglebtn = customtkinter.CTkButton(self.top, text = "Upload a NFT", command = lambda:self.NFT_home(1))
        self.NFTMultibtn = customtkinter.CTkButton(self.top, text = "Upload Multiple NFT", command = lambda:self.NFT_home(2))
        self.NFTIMGbtn = customtkinter.CTkButton(self.top, text = "NFT Image", command = self.NFT_img)
        self.NFTMETAbtn = customtkinter.CTkButton(self.top, text = "NFT Metadata", command = self.NFT_Meta)
        self.NFTNameLB = customtkinter.CTkEntry(self.top,height = 25, width = 300,placeholder_text="NFT Name")
        self.NFTSYMLB = customtkinter.CTkEntry(self.top,height = 25, width = 300,placeholder_text="NFT Symbol")
        self.NFTDescLB = customtkinter.CTkEntry(self.top,height = 25, width = 300,placeholder_text="NFT Description")
        self.NFTATTLB = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="NFT Attributes Type (optional)")
        self.NFTATTvalLB = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="NFT Attributes Value (optional)")
        self.NFTcollectionLB = customtkinter.CTkEntry(self.top,height = 25, width = 300,placeholder_text="Add to collection (optional)")
        self.NFTUploadbtn = customtkinter.CTkButton(self.top, text = "UPLOAD NFT", command = self.NFT_Upload)
        self.NFTimgFile =""
        self.NFTRoyalites = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Royialties %")
        self.ArweaveWalletbtn = customtkinter.CTkButton(self.top, text = "Connect your Arweave Wallet", command = self.Arweave_wallet)
        self.IMGBLKBTN = customtkinter.CTkButton(self.top, text ='Select folder of NFTs', command = self.IMGBLK)
        self.MetaBLKBTN = customtkinter.CTkButton(self.top, text ='Select folder of Metadata', command = self.MetaBLK)
        
        self.ValMonBTN = customtkinter.CTkButton(self.top, text ='Validator Monitor', command = self.ValMon)
        self.ValID = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Validator ID")
        self.ValVOTE = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Validator VOTE")
        self.ValVIDWarn = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Validator ID Warn Amount")
        self.ValVOTEWarn = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Validator VOTE Warn Amount")
        self.DiscWebHock = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Discord webhock")
        self.ValMonMonitorBTN = customtkinter.CTkButton(self.top, text ='Monitor Validator', command = self.ValMonMonitor)
        self.Val_var = tkinter.IntVar()
        self.ValChoise1 = customtkinter.CTkRadioButton(master=self.top, text="Monitor Your Validator",command=self.ValChoise, variable= self.Val_var, value=1)
        self.ValChoise2 = customtkinter.CTkRadioButton(master=self.top, text="Monitor Someone else Validator",command=self.ValChoise, variable= self.Val_var, value=2)

        self.addTokenMetaBTN = customtkinter.CTkButton(self.top, text ='Add token to Reg', command = self.TokenReg)
        self.TKNname = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Token Name")
        self.TKNticker = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Token Ticker")
        self.TKNimg = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Token Img URL")
        self.TKNDSK = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Token Desicription")
        self.addTokeRegBTN = customtkinter.CTkButton(self.top, text ='Redgister Token', command = self.Tokenreq)

        self.ChainMonBTN = customtkinter.CTkButton(self.top, text ='Chain Monitor', command = self.ChainMonitor)
        self.ValInfoBTN = customtkinter.CTkButton(self.top, text ='Validator Info', command = self.GetValidators)
    
        
    def Run(self):
        self.HomePage()
        while True:
            self.top.update()
            if(self.wallet_connected == True):
                Sec = int(strftime("%S", gmtime()))
                if(Sec == 15 or Sec == 30 or Sec == 45 or Sec == 59):
                    self.WalletBal()                
            
        
    def TKN_NFT(self,typ):
        self.TKNorNFT = typ
        self.NFTbtn.place_forget()
        self.TKNbtn.place_forget()
        self.ChainMonBTN.place_forget()
        self.ValMonBTN.place_forget()
        self.HomePage()
        
    def WalletBal(self):
        if(self.client.is_connected()):
            resp = self.client.get_balance(self.keypair.public_key)
            bal = int(resp['result']['value']) / 1000000000
            #print("balance = ", bal)
            self.walletBal.configure(text="Ballance: %.4f Safe" % bal)
            self.top.update()
            (SafeValue, BWorth) = getLatestPrice(bal)
            self.SafeVal.configure(text="SafeCoin Price: %.4f USD" % SafeValue)
            self.walletVal.configure(text="Value: %.4f USD" % BWorth)
            self.top.update()
            
        else:
            print("Wallet connection ERROR")
            self.client = Client(self.EndPoint[self.Endpoint_selected])
            return 0
        
    def ClearHomepage(self):
        print("home reset")
        self.AirDropBTN.place_forget()
        self.NFTMultibtn.place_forget()
        self.NFTSinglebtn.place_forget()
        self.TKNbtn.place_forget()
        self.NFTbtn.place_forget()
        self.TokenBTN.place_forget()
        self.Loadkey.place_forget()
        self.loadkeybtn.place_forget()
        self.loadkeyLB.place_forget()
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
        self.GetTokenBalbtn.place_forget()
        self.showWalletbtn.place_forget()
        self.loadkeyLB.place_forget()
        self.DevFeebtn.place_forget()
        self.NFTIMGbtn.place_forget()
        self.NFTMETAbtn.place_forget()
        self.NFTNameLB.place_forget()
        self.NFTSYMLB.place_forget()
        self.NFTDescLB.place_forget()
        self.NFTATTLB.place_forget()
        self.NFTATTvalLB.place_forget()
        self.NFTUploadbtn.place_forget()
        self.NFTcollectionLB.place_forget()
        self.NFTRoyalites.place_forget()
        self.ArweaveWalletbtn.place_forget()
        self.IMGBLKBTN.place_forget()
        self.MetaBLKBTN.place_forget()
        self.ValMonBTN.place_forget()
        self.ValChoise1.place_forget()
        self.ValChoise2.place_forget()
        self.ValMonMonitorBTN.place_forget()
        self.ValID.place_forget()
        self.ValVOTE.place_forget()
        self.ValVIDWarn.place_forget()
        self.ValVOTEWarn.place_forget()
        self.DiscWebHock.place_forget()
        self.addTokenMetaBTN.place_forget()
        self.TKNname.place_forget()
        self.TKNticker.place_forget()
        self.TKNimg.place_forget()
        self.addTokeRegBTN.place_forget()
        self.ChainMonBTN.place_forget()
        self.ValInfoBTN.place_forget()
        self.TokenText.delete(tkinter.END)
        self.TKNorNFT=0
        self.HomePage()
    
    def HomePage(self):
        wallet_exists = exists('KeyPair.json')
        self.HomePagebtn.place(x=740, y=460)
        if(self.wallet_connected == False):
            if(wallet_exists):
                text ="Wallet Connect"
                command = self.WalletConnect
                self.DeleteKeybtn.place(x=350, y=10)
                
            else:
                text ="Create New Wallet"
                command = self.walletNew
                
                self.loadkeyLB.place(x=10, y=100)
                self.Loadkey.place(x=100, y=100)
                self.loadkeybtn.place(x=100, y=130)
                self.showWalletbtn.place_forget()
            
            self.wallet = customtkinter.CTkButton(self.top, text =text, command = command)
            self.wallet.place(x=10, y=50)
            opt = ["Mainnet", "Testnet", "Devnet"]
            self.Endpoint_Drop = customtkinter.CTkOptionMenu(self.top, variable=self.EndpintVar,values=opt,command=self.NetworkChange)    
            self.Endpoint_Drop.place(x=10, y=8)
   
        else:
            if(self.OwnMint==False and self.EndPoint[self.Endpoint_selected]== 'https://api.mainnet-beta.safecoin.org' ):
                text = "Please purchace this NFT to use this software on mainnet, Devnet and Testnet are free\n"
                tran = self.client.get_signatures_for_address('3TeRhNJj7rTMqHKx2znun9DfmgMh1KZaJbrbnzRg4Ttc')
                try:
                    for items in tran['result']: 
                            print(items['signature'])
                            res = self.client.get_confirmed_transaction(items['signature'])
                            #print(res)
                            mintowner = res['result']['meta']['postTokenBalances'][0]['owner']
                            #print(mintowner)
                            if(mintowner == str(self.keypair.public_key)):
                                print("you own the mint")
                                self.OwnMint=True
                                text = "Thankyou for owning the NFT to use this software\n"
                                break
                except:
                    print("Error")
                self.TokenText.insert(tkinter.END,text)
                        


            if(self.OwnMint==True or self.EndPoint[self.Endpoint_selected]== 'https://api.testnet.safecoin.org' or self.EndPoint[self.Endpoint_selected]== 'https://api.devnet.safecoin.org'):
                self.walletBal.place(x=10, y=80)
                self.SafeVal.place(x=160,y=450)
                self.walletVal.place(x=10,y=100)
                self.WalletBal()
                if(self.Endpoint_selected == 'Testnet' or self.Endpoint_selected == 'Devnet'):
                    self.AirDropBTN.place(x=180, y=80)
                else:
                    self.AirDropBTN.place_forget()
                self.showWalletbtn.place(x=180,y=10)
                self.DevFeebtn.place(x=10,y=450)
                if(self.TKNorNFT==0):# chose

                    self.NFTbtn.place(x=100, y=200)
                    self.TKNbtn.place(x=100, y=230)
                    self.ValMonBTN.place(x=100,y=260)
                    self.ChainMonBTN.place(x=100,y=290)
                    
                    
                elif(self.TKNorNFT==1):#Token
                    
                    self.TokenBTN.place(x=10, y=130)
                    self.TokenLoadBox.place(x=100, y=170)
                    self.TokenLoadLB.place(x=10, y=170)
                    self.TokenLoadbtn.place(x=100, y=200)

                elif(self.TKNorNFT==2):#NFT

                    self.NFTSinglebtn.place(x=100, y=200)
                    self.NFTMultibtn.place(x=100, y=230)
            else:
                self.TokenText.insert(tkinter.END,"Make sure the NFT is in the connected wallet\n")

                
    
        
    def NetworkChange(self,*args):
        self.Endpoint_selected = self.EndpintVar.get()
        print(self.Endpoint_selected)
        self.EndPoint[self.Endpoint_selected]
        self.EndpintVar.set(self.Endpoint_selected)
        self.client = Client(self.EndPoint[self.Endpoint_selected])
        print(self.EndPoint[self.Endpoint_selected])
        self.OwnMint=True
        self.ClearHomepage()

        
    def loadKey(self):
        key = self.Loadkey.get()
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
        self.wallet_connected = False
        self.wallet.place_forget()
        self.ClearHomepage()

    def Showimort(self):
        secret = [b for b in self.keypair.secret_key]
        print(secret)
        self.TokenText.insert(tkinter.END,"use this string to import into wallet.safecoin.org \n")
        self.TokenText.insert(tkinter.END,"%s \n" % secret)
        #self.TokenText.see("end")
        

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
        self.wallet.configure(text=self.keypair.public_key)
        self.ClearHomepage()


    def CreateToken(self):
        self.TokenText.insert(tkinter.END,"Creating a token and waiting for confirmation, Please wait .. \n")
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
                    #self.TokenText.see("end")
                    self.TokenBTN.place(x=200, y=200)
                    self.top.update()
                    return
                    
                
        print(resp)
        assert self.token_client.pubkey
        assert self.token_client.program_id == TOKEN_PROGRAM_ID
        assert self.token_client.payer.public_key == self.keypair.public_key
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)
        self.TokenText.insert(tkinter.END,"Token address = %s \n" % self.token_client.pubkey)
        #self.TokenText.see("end")
        self.TokenACCBTN.place(x=10, y=130)
        self.TokenLoadAccBox.place(x=150, y=170)
        self.TokenLoadAccbtn.place(x=100, y=200)
        self.TokenLoadlb.place(x=10, y=170)
        self.token_PubKey = self.token_client.pubkey
        return self.token_client

    def loadToken(self):
        
        token_PubKey = self.TokenLoadBox.get()
        self.token_PubKey = token_PubKey.strip('\n')
        print(self.token_PubKey)
        self.TokenText.insert(tkinter.END,"Loaded Token %s \n" % self.token_PubKey)
        #self.TokenText.see("end")
        self.TokenACCBTN.place(x=10, y=130)
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenBTN.place_forget()
        self.TokenLoadAccBox.place(x=150, y=170)
        self.TokenLoadAccbtn.place(x=100, y=200)
        self.TokenLoadlb.place(x=10, y=170)

    def loadTokenACC(self):
        token_Account = self.TokenLoadAccBox.get()
        self.token_Account = token_Account.strip('\n')
        print(self.token_Account)
        
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)

        self.TokenText.insert(tkinter.END,"Loaded Token Account %s \n" % self.token_Account)
        #self.TokenText.see("end")
        self.MintAntLB.place(x=10, y=170)
        self.MintBtn.place(x=100, y=200)
        self.AmountBox.place(x=100, y=170)
        self.AmountBox.delete(0,tkinter.END)
        self.AmountBox.insert(tkinter.END,"10")
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenACCBTN.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        self.TokenLoadlb.place_forget()
        self.addTokenMetaBTN.place(x=10, y=240)
        self.GetTokenBalbtn.place(x=10, y=130)
        
        
    def CreateAcount(self):
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        print(self.token_PubKey)
        
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenACCBTN.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        
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
                    #self.TokenText.see("end")
                    self.TokenACCBTN.place(x=10, y=130)
                    self.TokenLoadAccBox.place(x=150, y=170)
                    self.TokenLoadAccbtn.place(x=100, y=200)
                    self.TokenLoadlb.place(x=10, y=170)
                    self.top.update()
                    return
        print(resp)
        print(self.token_Account)
        self.MintAntLB.place(x=10, y=170)
        self.MintBtn.place(x=100, y=200)
        self.AmountBox.place(x=100, y=170)
        self.AmountBox.delete(0,tkinter.END)
        self.AmountBox.insert(tkinter.END,"10")
        self.GetTokenBalbtn.place(x=10, y=130)
        self.TokenText.insert(tkinter.END,"Creating a token Account created %s \n" % self.token_Account)
        #self.TokenText.see("end")
        self.addTokenMetaBTN.place(x=10, y=240)
        self.top.update()
        return self.token_Account

    def GetTokenBalance(self):
        print(self.token_Account)
        TokenBall = self.TokenACCOUNT.get_balance(pubkey=self.token_Account)
        print(TokenBall)
        if('error' not in TokenBall):
            self.TokenText.insert(tkinter.END,"Token Ballance = %s \n" % int(TokenBall['result']['value']['uiAmount']))
        else:
            self.TokenText.insert(tkinter.END,"Token Ballance Error, please check keypairs \n")

    def DevFee(self):
        txn = Transaction().add(transfer(TransferParams(from_pubkey=self.keypair.public_key, to_pubkey="JoNVxV8vwBdHqLJ2FT4meLupYKUVVDYr1Pm4DJUp8cZ", lamports=999998000)))
        snd = self.client.send_transaction(txn, self.keypair)
        print(snd)
        self.TokenText.insert(tkinter.END,"Sending 1 safecoin")
        gotTX = self.await_TXN_full_confirmation(self.client,snd['result'])
        if(gotTX):
            self.TokenText.insert(tkinter.END,"Thankyou for your support, appreciate all the donations, keeps me making free open source programs \n")       
        else:
            print("Tip Failed")
            self.TokenText.insert(tkinter.END,"Tip Failed\n")

        
        #self.TokenText.see("end")

    def MintToken(self, amount = 10):
        amount = int(self.AmountBox.get())
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
            gotTX = self.await_TXN_full_confirmation(self.client,resp['result'])
            print("tx : ",gotTX)
            if(gotTX):
                print(amount, " tokens minted, tx = ",resp['result'])
                self.TokenText.insert(tkinter.END,"Minted %s Tokens completed\n" % amount)       
            else:
                print("Tokens Failed to mint")
                self.TokenText.insert(tkinter.END,"Tokens Failed to mint please try again\n")
            self.top.update()
                
        else:
            print("please use just numbers")
            self.TokenText.insert(tkinter.END,"please just use numbers")
            #self.TokenText.see("end")
            self.top.update()

    def TokenReg(self):
        self.MintAntLB.place_forget()
        self.MintBtn.place_forget()
        self.AmountBox.place_forget()
        self.GetTokenBalbtn.place_forget()
        self.addTokenMetaBTN.place_forget()
        self.TKNname.place(x=10, y=150)
        self.TKNticker.place(x=10, y=180)
        self.TKNimg.place(x=10, y=210)
        self.TKNDSK.place(x=10, y=240)
        self.addTokeRegBTN.place(x=10, y=270)

    def Tokenreq(self):
        TokenName = self.TKNname.get()
        TokenTicker = self.TKNticker.get()
        TokenImgURL = self.TKNimg.get()
        TokenDSK = self.TKNDSK.get()
        if(len(TokenName) == 0):
            self.TKNname.configure(placeholder_text_color='red')
            return
        if(len(TokenTicker) == 0):
            self.TKNticker.configure(placeholder_text_color='red')
            return
        if(len(TokenImgURL) == 0):
            self.TKNimg.configure(placeholder_text_color='red')
            return
        if(len(TokenDSK) == 0):
            TokenDSK = None
            return
            
        self.TokenText.insert(tkinter.END,"Trying to reqister token on chanin please wait ..\n")
        self.TKNname.place_forget()
        self.TKNticker.place_forget()
        self.TKNimg.place_forget()
        self.addTokeRegBTN.place_forget()

        ###########################################################################################


        returnarweaveURL = {"name": TokenName,
          "symbol": TokenTicker,
          "description": TokenDSK,
          "image": TokenImgURL
        }##need to upload this metadta to arweave

        ######arweave upload image then ARWEAVE metadata then below
        
        metadataPDA = str(self.keypair.public_key)# need to work out
        tokenMetadata = { "name": TokenName,"symbol": TokenTicker,"image": returnarweaveURL}
        sendDic = {'metadata': metadataPDA,
            'metadataData': tokenMetadata,
            'updateAuthority': str(self.keypair.public_key),
            'mint': self.token_PubKey,
            'mintAuthority': str(self.keypair.public_key),
            "sellerFeeBasisPoints": 0,
            "creators": null,
            "collection": null,
            "uses": null}
        
        print(sendDic)
        print(json.dumps(sendDic))
        

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
            self.TokenText.insert(tkinter.END,".")
            self.top.update()
            if resp["result"]:
                print(f"Took {elapsed} seconds to confirm transaction {txn}")
                self.TokenText.insert(tkinter.END,"\n" )
                gotTX = True
                return True
        
        self.TokenText.insert(tkinter.END,"\n")        
        return gotTX

    def airdrop(self):
        resp = {}
        if(self.client.is_connected()):
            self.TokenText.insert(tkinter.END,"Air dropping 1 safe, please wait for it to confirm\n")
            #self.TokenText.see("end")
            self.top.update()
            while 'result' not in resp:
                resp = self.client.request_airdrop(self.keypair.public_key,1000000000)
            txn = resp['result']
            self.await_full_confirmation(self.client, txn)
            print(resp)
            print("Topup complete")
            self.TokenText.insert(tkinter.END,"Air drop completed tx = %s \n" % txn)
            #self.TokenText.see("end")
        else:
            print("not connected to %s"%self.api_endpoint)




###########################################Token above NFT below share wallet connection, need to separtate out into smaller files in V2 but this will do for now ###################################

    def NFT_home(self,typ):#1 = single 2 = multiple
        self.NFTMultibtn.place_forget()
        self.NFTSinglebtn.place_forget()
        self.ArweaveWalletbtn.place(x=10, y=170)
        if(typ == 1 ):

            self.NFTIMGbtn.place(x=10, y=200)
            #self.NFTMETAbtn.place(x=100, y=230)
            self.NFTNameLB.place(x=10, y=230)
            self.NFTSYMLB.place(x=10, y=260)
            self.NFTDescLB.place(x=10, y=290)
            self.NFTATTLB.place(x=10, y=320)
            self.NFTATTvalLB.place(x=160, y=320)
            self.NFTcollectionLB.place(x=10, y=350)
            self.NFTRoyalites.place(x=160, y=380)


        elif(typ == 2):
            
            self.IMGBLKBTN.place(x=10, y=200)
            self.MetaBLKBTN.place(x=10, y=230)

    def IMGBLK(self):
        IMG_Folder = filedialog.askdirectory()
    
    def MetaBLK(self):
        Meta_Folder = filedialog.askdirectory()
    
    def NFT_img(self):
        self.NFTimgFile = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = [("NFT Images","*.jpg;*.png")])
        self.TokenText.insert(tkinter.END,"NFT Image Selected: %s \n" % self.NFTimgFile)
        self.NFTIMGbtn.configure(fg_color='green')


    def NFT_Meta(self):
        filename = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = ("Text files","*.json"))

    def NFT_Upload(self):
            
        name = self.NFTNameLB.get()
        SYM = self.NFTSYMLB.get()
        Des = self.NFTDescLB.get()
        ATT = self.NFTATTLB.get()
        ATTval = self.NFTATTvalLB.get()
        COLL = self.NFTcollectionLB.get()
        Royal = self.NFTRoyalites.get()
        
        if(len(self.NFTimgFile) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please select a NFT image \n")
            self.NFTIMGbtn.configure(fg_color='red')
        elif(len(name) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter name \n")
            self.NFTNameLB.configure(placeholder_text_color='red')
        elif(len(SYM) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Symbol \n")
            self.NFTSYMLB.configure(placeholder_text_color='red')
        elif(len(Des) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Description \n")
            self.NFTDescLB.configure(placeholder_text_color='red')
        elif(len(Royal) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Royalties \n")
            self.NFTRoyalites.configure(placeholder_text_color='red')
        else:

            if(len(ATT) <= 0 ):
                ATT = None
            else:
                ATTsplit = ATT.split(',')
                ATTvalSplit = ATTval.split(',')
                ATT = []
                i = 0
                for x in ATTsplit:
                        ATT.append({x:ATTvalSplit[i]})
                        i =+ 1 
            #print(ATT)    
            if(len(ATTval) <= 0 ):
                ATTval = None
            if(len(COLL) <= 0 ):
                COLL = None
            if(Royal != 0):
                Royal = int(Royal) * 100

            AweaveURL = "" ######################### need to sort###################
            FileType = "png" ######################### need to sort###################
            
            tx = arweaveUpload(self.NFTimgFile, "image/%s" % FileType)
            
            print("creating Meta and uploading to arweave and ledamint")
            MetaData = json.dumps({"name": name, "symbol": SYM, "description": Des, "seller_fee_basis_points": Royal,
                        "image": AweaveURL,
                        "attributes": ATT, "external_url": "",
                        "properties": {"files": [{"uri": AweaveURL, "type": "image/%s" % FileType}],
                                       "category": "image", "creators": [{"address": str(self.keypair.public_key), "share": 100}]},
                        "collection": COLL, "use": None})
            print(MetaData)

    def Arweave_wallet(self):
        arweaveWallet = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = [("Arweave Wallet","*.json")])
        if(len(arweaveWallet) > 0):
            self.TokenText.insert(tkinter.END,"Arweave wallet selected: %s \n" % self.arweaveWallet)
            self.ArweaveWallet = arweave.Wallet(arweaveWallet)
            self.NFTUploadbtn.place(x=10, y=380)

    def arweaveUpload(self,fileLocaliton, DataType):
        with open(fileLocaliton, "rb", buffering=0) as file_handler:
            tx = Transaction(self.ArweaveWallet, file_handler=file_handler, file_path=fileLocaliton)
            tx.add_tag('Content-Type', DataType)
            tx.sign()

            uploader = get_uploader(tx, file_handler)

            while not uploader.is_complete:
                uploader.upload_chunk()

                logger.info("{}% complete, {}/{}".format(
                    uploader.pct_complete, uploader.uploaded_chunks, uploader.total_chunks
                ))
            print(tx.get_status())
        
    def await_full_confirmation(self,client, txn, max_timeout=60):
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


##################################################################validator monitor########################################################################
###########################################################################################################################################################

    def ValMon(self):
        self.TKNbtn.place_forget()
        self.NFTbtn.place_forget()
        self.ValMonBTN.place_forget()
        self.ChainMonBTN.place_forget()
        self.ValChoise1.place(x=10, y=130)
        self.ValChoise2.place(x=10, y=160)
        
        
    def ValChoise(self):
        
        if(self.Val_var.get() == 1):
            
            self.ValID.place(x=10, y=190)
            self.ValVOTE.place(x=10, y=220)
            self.ValVIDWarn.place(x=10, y=250)
            self.ValVOTEWarn.place(x=10, y=280)
            self.DiscWebHock.place(x=10, y=310)
            self.ValMonMonitorBTN.place(x=10, y=340)
            self.ValMonMonitorBTN.configure(command = self.ValMonMonitor)
        else:
            self.ValID.place(x=10, y=190)
            self.ValID.configure(placeholder_text="Validator ID's")
            self.TokenText.insert(tkinter.END,"Monitor More then 1 validator by placing a , between there ID's\n")
            self.DiscWebHock.place(x=10, y=220)
            self.ValMonMonitorBTN.place(x=10, y=250)
            self.ValVOTEWarn.place_forget()
            self.ValVIDWarn.place_forget()
            self.ValMonMonitorBTN.configure(command = self.otherValMonMonitor)
            

    def ValMonMonitor(self):
        
        ValidatorID = self.ValID.get()
        ValidatorVote = self.ValVOTE.get()
        IdentityBalanceWarn = self.ValVIDWarn.get()
        VoteBalanceWarn = self.ValVOTEWarn.get()
        Discord_Web_Hock = self.DiscWebHock.get()

        
        if(len(ValidatorID) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter validator ID pubkey\n")
            self.ValID.configure(placeholder_text_color='red')
        elif(len(ValidatorVote) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Validator Vote Pubkey\n")
            self.ValVOTE.configure(placeholder_text_color='red')
        elif(len(IdentityBalanceWarn) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter ID Warn Amount \n")
            self.ValVIDWarn.configure(placeholder_text_color='red')
        elif(len(VoteBalanceWarn) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Vote Warn Amount \n")
            self.ValVOTEWarn.configure(placeholder_text_color='red')
        elif(len(Discord_Web_Hock) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Discord WebHock \n")
            self.DiscWebHock.configure(placeholder_text_color='red')
        else:
            self.ValID.place_forget()
            self.ValVOTE.place_forget()
            self.ValVIDWarn.place_forget()
            self.ValVOTEWarn.place_forget()
            self.DiscWebHock.place_forget()
            self.ValMonMonitorBTN.place_forget()
            preMin = 99
            VM = ValidatorMonitor.ValidatorMonitor(Discord_Web_Hock,ValidatorID)
            self.TokenText.insert(tkinter.END,"Monitoring your validators \n")
            while True:
                self.top.update()
                Min = strftime("%M", gmtime())
                if(preMin != Min):
                    VM.MYMonitor(self.EndPoint[self.Endpoint_selected],self.client,ValidatorID,ValidatorVote,int(VoteBalanceWarn),int(IdentityBalanceWarn))
                    preMin = Min

    def otherValMonMonitor(self):
        
        ValidatorID = self.ValID.get()
        print(ValidatorID)
        Discord_Web_Hock = self.DiscWebHock.get()
        print(Discord_Web_Hock)
        ValidatorIDs = ValidatorID.split(',')
        
        if(len(ValidatorID) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter validator ID pubkey\n")
            self.ValID.configure(placeholder_text_color='red')
        elif(len(Discord_Web_Hock) <= 0 ):
            self.TokenText.insert(tkinter.END,"Please enter Discord WebHock \n")
            self.DiscWebHock.configure(placeholder_text_color='red')
        else:
            self.ValID.place_forget()
            self.DiscWebHock.place_forget()
            self.ValMonMonitorBTN.place_forget()
            preMin = 99

            VM = ValidatorMonitor.ValidatorMonitor(Discord_Web_Hock,ValidatorIDs)
            self.TokenText.insert(tkinter.END,"Monitoring validators \n")
            while True:
                self.top.update()
                Min = strftime("%M", gmtime())
                if(preMin != Min):
                    VM.OtherMonitor(self.EndPoint[self.Endpoint_selected],self.client,ValidatorIDs)
                    preMin = Min


########################################################################################################################################################################################

    def ChainMonitor(self):
        self.NFTbtn.place_forget()
        self.TKNbtn.place_forget()
        self.ValMonBTN.place_forget()
        self.ChainMonBTN.place_forget()
        self.ValInfoBTN.place(x=100, y=200)

    def GetValidators(self):
        VI = ValidatorMonitor.validatorInfo(self.client)
        VI.getVal(self.TokenText,tkinter)
        #VI.get_stake_activation()
        

        
Safe_Token = Safecoin_Token()
Safe_Token.Run()


