import argparse
import string
import random
import json
import time
import base58
import base64
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
from arweave.utils import winston_to_ar
import customtkinter
from time import gmtime, strftime
import json
import ValidatorMonitor
from coinGeko import getLatestPrice,getLatestPriceArweave,getLatestPriceSafecoin
import requests



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
        self.top.geometry("1000x500")
        self.wallet_connected = False
        self.EndpintVar = tkinter.StringVar(self.top)
        self.EndpintVar.set("Mainnet")
        
        self.AirDropBTN = customtkinter.CTkButton(self.top, text ='Airdrop 1 safecoin', command = self.airdrop)
        self.TokenText = customtkinter.CTkTextbox(self.top,height = 400, width = 480)
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
        
        self.TKNimg = customtkinter.CTkButton(self.top, text="Token Img",command = self.TokenImg)
        self.TKNDSK = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Token Desicription")
        self.addTokeRegBTN = customtkinter.CTkButton(self.top, text ='Redgister Token', command = self.Tokenreq)
        self.addTokeBurnBTN = customtkinter.CTkButton(self.top, text ='Token Burn', command = self.TokenBurn)
        self.TKNBurnAmount = customtkinter.CTkEntry(self.top,height = 25, width = 150,placeholder_text="Burn Amount")
        self.FreezeBTN = customtkinter.CTkButton(self.top, text ='Token Freeze', command = self.TokenFreeze)
        self.ThawBTN = customtkinter.CTkButton(self.top, text ='Token Thaw', command = self.TokenThaw)

        
        self.ChainMonBTN = customtkinter.CTkButton(self.top, text ='Chain Monitor', command = self.ChainMonitor)
        self.ValInfoBTN = customtkinter.CTkButton(self.top, text ='Validator Info', command = self.GetValidators)
        self.ValStakeBTN = customtkinter.CTkButton(self.top, text ='Validator Stake info', command = self.GetValStake)
        self.ClearTxtBTN = customtkinter.CTkButton(self.top, text ='Clear', command = self.ClearTxt)
        self.LrgAccountsBTN = customtkinter.CTkButton(self.top, text ='Get Largest Accounts', command = self.LrgAcc)

        
        
    def Run(self):
        self.HomePage()
        once = 1
        while True:
            self.top.update()
            if(self.wallet_connected == True):
                Sec = int(strftime("%S", gmtime()))
                if(Sec == 15 or Sec == 30 or Sec == 45 or Sec == 59):
                    if(once == 1):
                        once = 0
                        self.WalletBal()
                else:
                    once = 1
            
        
    def TKN_NFT(self,typ):
        self.TKNorNFT = typ
        self.NFTbtn.place_forget()
        self.TKNbtn.place_forget()
        self.ChainMonBTN.place_forget()
        self.ValMonBTN.place_forget()
        self.HomePage()

    def ClearTxt(self):
        self.TokenText.delete('1.0', tkinter.END)
        
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
            self.TokenText.insert('1.0',"Error getting wallet ballance and not connected to %s\n" % self.EndPoint[self.Endpoint_selected])
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
        self.ValStakeBTN.place_forget()
        self.LrgAccountsBTN.place_forget()
        self.NFTDescLB.place_forget()
        self.addTokeBurnBTN.place_forget()
        self.TKNBurnAmount.place_forget()
        self.FreezeBTN.place_forget()
        self.ThawBTN.place_forget()
        self.TKNorNFT=0
        self.HomePage()
    
    def HomePage(self):
        wallet_exists = exists('KeyPair.json')
        self.HomePagebtn.place(x=740, y=460)
        self.ClearTxtBTN.place(x=650, y=420)
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
                self.TokenText.insert('1.0',text)
                        


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
                self.TokenText.insert('1.0',"Make sure the NFT is in the connected wallet\n")

                
    
        
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
        self.TokenText.insert('1.0',"use this string to import into wallet.safecoin.org \n")
        self.TokenText.insert('1.0',"%s \n" % secret)
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
        self.TokenText.insert('1.0',"Creating a token and waiting for confirmation, Please wait .. \n")
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
            freeze_authority = self.keypair.public_key,
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
                    self.TokenText.insert('1.0',"Creating a token Failed Please try again \n")
                    #self.TokenText.see("end")
                    self.TokenBTN.place(x=200, y=200)
                    self.top.update()
                    return
                    
                
        print(resp)
        assert self.token_client.pubkey
        assert self.token_client.program_id == TOKEN_PROGRAM_ID
        assert self.token_client.payer.public_key == self.keypair.public_key
        assert resp["result"]["value"]["owner"] == str(TOKEN_PROGRAM_ID)
        self.TokenText.insert('1.0',"Token address = %s \n" % self.token_client.pubkey)
        #self.TokenText.see("end")
        self.TokenACCBTN.place(x=10, y=130)
        self.TokenLoadAccBox.place(x=150, y=170)
        self.TokenLoadAccbtn.place(x=100, y=200)
        self.TokenLoadlb.place(x=10, y=170)
        self.FreezeBTN.place(x=10, y=300)
        self.ThawBTN.place(x=10, y=330)
        self.token_PubKey = self.token_client.pubkey
        return self.token_client

    def loadToken(self):
        
        token_PubKey = self.TokenLoadBox.get()
        self.token_PubKey = token_PubKey.strip('\n')
        print(self.token_PubKey)
        self.TokenText.insert('1.0',"Loaded Token %s \n" % self.token_PubKey)
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

        self.TokenText.insert('1.0',"Loaded Token Account %s \n" % self.token_Account)
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
        self.addTokeBurnBTN.place(x=10, y=270)
        self.TKNBurnAmount.place(x=200, y=270)
        self.FreezeBTN.place(x=10, y=300)
        self.ThawBTN.place(x=10, y=330)
        
        
    def CreateAcount(self):
        self.TokenACCOUNT = Token(conn=self.client,pubkey=self.token_PubKey,program_id=TOKEN_PROGRAM_ID,payer=self.keypair)
        print(self.token_PubKey)
        self.TokenLoadLB.place_forget()
        self.TokenLoadBox.place_forget()
        self.TokenLoadbtn.place_forget()
        self.TokenACCBTN.place_forget()
        self.TokenLoadAccBox.place_forget()
        self.TokenLoadAccbtn.place_forget()
        
        self.token_Account = self.TokenACCOUNT.create_associated_token_account(self.token_PubKey,skip_confirmation = True)
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
                    self.TokenText.insert('1.0',"Creating a token Account Failed Please try again \n")
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
        self.TokenLoadlb.place_forget()
        self.GetTokenBalbtn.place(x=10, y=130)
        self.TokenText.insert('1.0',"Creating a token Account created %s \n" % self.token_Account)
        #self.TokenText.see("end")
        self.addTokenMetaBTN.place(x=10, y=240)
        self.addTokeBurnBTN.place(x=10, y=270)
        self.TKNBurnAmount.place(x=200, y=270)
        self.top.update()
        return self.token_Account

    def GetTokenBalance(self):
        print(self.token_Account)
        TokenBall = self.TokenACCOUNT.get_balance(pubkey=self.token_Account)
        print(TokenBall)
        if('error' not in TokenBall):
            self.TokenText.insert('1.0',"Token Ballance = %s \n" % int(TokenBall['result']['value']['uiAmount']))
        else:
            self.TokenText.insert('1.0',"Token Ballance Error, please check keypairs \n")

    #26dhPSbqucjpuyaxsrucav93Av9AAeq5sz4aRFZMQAHz
    #8DwbfHPqg7AWwpbPKGstKpnzosxBDroS5kr7LWLSbhdR
    def TokenBurn(self):
        burnAmount = int(self.TKNBurnAmount.get())
        tx = self.TokenACCOUNT.burn(account=self.token_Account,owner=self.keypair,amount=burnAmount)
        print(tx)
        gotTX = self.await_TXN_full_confirmation(self.client,tx['result'])
        if(gotTX):
            self.TokenText.insert('1.0',"%s Token burnt \n"%burnAmount)       
        else:
            print("Tip Failed")
            self.TokenText.insert('1.0',"Burn Failed\n")
            
    def DevFee(self):
        txn = Transaction().add(transfer(TransferParams(from_pubkey=self.keypair.public_key, to_pubkey="JoNVxV8vwBdHqLJ2FT4meLupYKUVVDYr1Pm4DJUp8cZ", lamports=999998000)))
        snd = self.client.send_transaction(txn, self.keypair)
        print(snd)
        self.TokenText.insert('1.0',"Sending 1 safecoin")
        gotTX = self.await_TXN_full_confirmation(self.client,snd['result'])
        if(gotTX):
            self.TokenText.insert('1.0',"Thankyou for your support, appreciate all the donations, keeps me making free open source programs \n")       
        else:
            print("Tip Failed")
            self.TokenText.insert('1.0',"Tip Failed\n")

        
        #self.TokenText.see("end")

    def MintToken(self, amount = 10):
        amount = int(self.AmountBox.get())
        print("amount = ",amount)
        self.TokenText.insert('1.0',"Minting %s Tokens\n" % amount)
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
                self.TokenText.insert('1.0',"Minted %s Tokens completed\n" % amount)       
            else:
                print("Tokens Failed to mint")
                self.TokenText.insert('1.0',"Tokens Failed to mint please try again\n")
            self.top.update()
                
        else:
            print("please use just numbers")
            self.TokenText.insert('1.0',"please just use numbers")
            #self.TokenText.see("end")
            self.top.update()
    def TokenFreeze(self):
        self.popupFreezeWindow = customtkinter.CTkToplevel()
        self.popupFreezeWindow.geometry("400x200")
        self.popupFreezeWindow.wm_title("Are You Sure")
        labelBonus = customtkinter.CTkLabel(self.popupFreezeWindow, text="Are you sure you want to freeze")
        B2 = customtkinter.CTkButton(self.popupFreezeWindow, text="Yes", command=self.FreezeToken)
        B1 = customtkinter.CTkButton(self.popupFreezeWindow, text="No", command=self.popupFreezeWindow.destroy)
        B1.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        B2.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    def FreezeToken(self):
        self.popupFreezeWindow.destroy()
        resp = self.TokenACCOUNT.freeze_account(account=self.token_PubKey,authority=self.keypair)
        print(resp)
        gotTX = self.await_TXN_full_confirmation(self.client,resp['result'])
        if(gotTX):
            self.TokenText.insert('1.0',"Token Frozen \n")       
        else:
            print("Freeze Failed")
            self.TokenText.insert('1.0',"Freeze Failed\n")
            
    def TokenThaw(self):
        self.popupThawWindow = customtkinter.CTkToplevel()
        self.popupThawWindow.geometry("400x200")
        self.popupThawWindow.wm_title("Are You Sure")
        labelBonus = customtkinter.CTkLabel(self.popupThawWindow, text="Are you sure you want to Thaw")
        B2 = customtkinter.CTkButton(self.popupThawWindow, text="Yes", command=self.FreezeToken)
        B1 = customtkinter.CTkButton(self.popupThawWindow, text="No", command=self.popupThawWindow.destroy)
        B1.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        B2.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    def ThawToken(self):
        self.popupThawWindow.destroy()
        resp = self.TokenACCOUNT.thaw_account(account=self.token_Account,authority=self.keypair)
        print(resp)
        gotTX = self.await_TXN_full_confirmation(self.client,resp['result'])
        if(gotTX):
            self.TokenText.insert('1.0',"Token Thawed \n")       
        else:
            print("Thaw Failed")
            self.TokenText.insert('1.0',"Thaw Failed\n")

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
        self.addTokeBurnBTN.place_forget()
        self.TKNBurnAmount.place_forget()

    def Tokenreq(self):
        TokenName = self.TKNname.get()
        TokenTicker = self.TKNticker.get()
        
        TokenDSK = self.TKNDSK.get()
        if(len(TokenName) == 0):
            self.TKNname.configure(placeholder_text_color='red')
            return
        if(len(TokenTicker) == 0):
            self.TKNticker.configure(placeholder_text_color='red')
            return
        if(len(self.TokenFileName) == 0):
            self.TKNimg.configure(text_color='red')
            return
        if(len(TokenDSK) == 0):
            TokenDSK = None
            return
            
        self.TokenText.insert('1.0',"Trying to reqister token on chain please wait ..\n")
        self.TKNname.place_forget()
        self.TKNticker.place_forget()
        self.TKNimg.place_forget()
        self.addTokeRegBTN.place_forget()
        self.TKNDSK.place_forget()

        ###########################################################################################

        arweavePrice = getLatestPriceArweave()
        SafecoinPrice = getLatestPriceSafecoin()
        exchangeRate = arweavePrice / SafecoinPrice
        AR_FEE_MULTIPLIER = 20 / 100
        
            
        with open(self.TokenFileName,"rb") as f:
            f_bytes = f.read()
        f_b64 = base64.b64encode(f_bytes).decode("utf8")

        
        tokenimgSize = os.path.getsize(self.TokenFileName)
        #print("image size %s" % tokenimgSize)

        API_URL = "https://arweave.net"
        url = "{}/price/{}".format(API_URL, tokenimgSize)

        response = requests.get(url)

        if response.status_code == 200:
             #print("Cost in winston %s " % response.text)
             TokenimgCost = winston_to_ar(response.text)
        else:
            self.TokenText.insert('1.0',"Unable to get cost of Token image, Please try again\n")
            return
        #print("TokenCost %s" % TokenimgCost)
        #print("SafeAmount exact %s" % (exchangeRate * TokenimgCost))
        Safeamount = ((TokenimgCost * exchangeRate) * 15)
        #print("SafeAmount %s" %Safeamount)
        self.TokenText.insert('1.0',"\nToken image and metadata cost %s safe\n" % Safeamount)
        
        #workout amount and send safecoin to es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc so it can be converted to arweave

        txn = Transaction().add(transfer(TransferParams(from_pubkey=self.keypair.public_key, to_pubkey="es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc", lamports=int(Safeamount * 1000000000))))
        snd = self.client.send_transaction(txn, self.keypair)
        print(snd)
        gotTX = self.await_TXN_full_confirmation(self.client,snd['result'])
        if(gotTX):
            self.TokenText.insert('1.0',"Safecoin sent and converted for storage on arweave, uploading image and metadata\n")       
        else:
            self.TokenText.insert('1.0',"Sending safecoin for upload failed please try again\n")
            return
           
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
        
        ImgType = self.TokenFileName.split('.')[1]
        payload = json.dumps({"metadata":sendDic, "env":self.EndPoint[self.Endpoint_selected],'transaction':snd['result'],'image':f_b64,'type':ImgType})
        #print(payload)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post("https://onestopshop.ledamint.io", verify=False,data=payload,headers=headers)
        #response = requests.post("https://onestopshop.ledamint.io",data=payload, headers=headers)

        #print(response.content.decode())
        res = (json.loads(response.text.split('\r\n\r\n')[1])['MetaLink'])
        
        if(res == 'ERROR'):
            print('Didnt recive safecoin in arweave wallet')
            return
        self.TokenText.insert('1.0',"\n" )
        self.TokenText.insert('1.0',res)
        self.TokenText.insert('1.0',"Arweave Token reg URL: ")
        self.TokenText.insert('1.0',"\n")

        cfg = {
            "PRIVATE_KEY": base58.b58encode(self.keypair.seed).decode("ascii"),
            "PUBLIC_KEY": str(self.keypair.public_key),
            "DECRYPTION_KEY": Fernet.generate_key().decode("ascii"),
        }
        #print(cfg)
        api = LedamintAPI(cfg)
        result = api.deploy(self.EndPoint[self.Endpoint_selected], TokenName, TokenTicker,0)
        contract_key = json.loads(result).get('contract')
        # conduct a mint, and send to a recipient, e.g. wallet_2
        mint_res = api.mint(self.EndPoint[self.Endpoint_selected], contract_key, self.token_Account, res)

        
    def TokenImg(self):
        self.TokenFileName = filedialog.askopenfilename(initialdir = "/",title = "Select a File",filetypes = [("Image","*.jpg;*.png")])
        self.TokenText.insert('1.0',"\n" )
        self.TokenText.insert('1.0',self.TokenFileName)
        self.TokenText.insert('1.0',"\n")
        
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
            self.TokenText.insert('1.0',".")
            self.top.update()
            if resp["result"]:
                print(f"Took {elapsed} seconds to confirm transaction {txn}")
                self.TokenText.insert('1.0',"\n" )
                gotTX = True
                return True
        
        self.TokenText.insert("1.0","\n")        
        return gotTX

    def airdrop(self):
        resp = {}
        if(self.client.is_connected()):
            self.TokenText.insert('1.0',"Air dropping 1 safe, please wait for it to confirm\n")
            #self.TokenText.see("end")
            self.top.update()
            while 'result' not in resp:
                resp = self.client.request_airdrop(self.keypair.public_key,1000000000)
            txn = resp['result']
            self.await_full_confirmation(self.client, txn)
            print(resp)
            print("Topup complete")
            self.TokenText.insert('1.0',"Air drop completed tx = %s \n" % txn)
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
        self.TokenText.insert('1.0',"NFT Image Selected: %s \n" % self.NFTimgFile)
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
            self.TokenText.insert('1.0',"Please select a NFT image \n")
            self.NFTIMGbtn.configure(fg_color='red')
        elif(len(name) <= 0 ):
            self.TokenText.insert('1.0',"Please enter name \n")
            self.NFTNameLB.configure(placeholder_text_color='red')
        elif(len(SYM) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Symbol \n")
            self.NFTSYMLB.configure(placeholder_text_color='red')
        elif(len(Des) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Description \n")
            self.NFTDescLB.configure(placeholder_text_color='red')
        elif(len(Royal) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Royalties \n")
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
            self.TokenText.insert('1.0',"Arweave wallet selected: %s \n" % self.arweaveWallet)
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
            self.TokenText.insert('1.0',"Monitor More then 1 validator by placing a , between there ID's\n")
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
            self.TokenText.insert('1.0',"Please enter validator ID pubkey\n")
            self.ValID.configure(placeholder_text_color='red')
        elif(len(ValidatorVote) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Validator Vote Pubkey\n")
            self.ValVOTE.configure(placeholder_text_color='red')
        elif(len(IdentityBalanceWarn) <= 0 ):
            self.TokenText.insert('1.0',"Please enter ID Warn Amount \n")
            self.ValVIDWarn.configure(placeholder_text_color='red')
        elif(len(VoteBalanceWarn) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Vote Warn Amount \n")
            self.ValVOTEWarn.configure(placeholder_text_color='red')
        elif(len(Discord_Web_Hock) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Discord WebHock \n")
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
            self.TokenText.insert('1.0',"Monitoring your validators \n")
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
            self.TokenText.insert('1.0',"Please enter validator ID pubkey\n")
            self.ValID.configure(placeholder_text_color='red')
        elif(len(Discord_Web_Hock) <= 0 ):
            self.TokenText.insert('1.0',"Please enter Discord WebHock \n")
            self.DiscWebHock.configure(placeholder_text_color='red')
        else:
            self.ValID.place_forget()
            self.DiscWebHock.place_forget()
            self.ValMonMonitorBTN.place_forget()
            preMin = 99

            VM = ValidatorMonitor.ValidatorMonitor(Discord_Web_Hock,ValidatorIDs)
            self.TokenText.insert('1.0',"Monitoring validators \n")
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
        self.VI = ValidatorMonitor.validatorInfo(self.client)
        self.valdata = self.VI.getVal()
        #print(self.valdata)
        for k,v in self.valdata.items():
            self.TokenText.insert('1.0',"%s\nCommission:%s  Stake:%s \n \n" %(k,v['Com'],v['stake']))
        self.ValStakeBTN.place(x=100, y=230)
        self.LrgAccountsBTN.place(x=100, y=260)

    def GetValStake(self):
        for k,v in self.valdata.items():
            #print(k,v)
            stakeData = self.VI.get_stake_activation(k)
            #print(k)
            #print(stakeData)
            #print(stakeData['result']['active'])
            #print(stakeData['result']['inactive'])
            self.TokenText.insert('1.0',"%s\nStake Active:%s  deactive:%s \n \n" %(k,stakeData['result']['active'],stakeData['result']['inactive']))

    def LrgAcc(self):
        LrgAcc = self.client.get_largest_accounts()['result']['value']
        #LrgAcc = LrgAcc.split('}, {')
        
        for i in range(20):
            #print(LrgAcc[i]['address'])
            #print(LrgAcc[i]['lamports'])
            self.TokenText.insert('1.0',"%s : %s \n" %(LrgAcc[i]['address'],LrgAcc[i]['lamports']))
        self.TokenText.insert('1.0',"largest accounts \n")
        #print(LrgAcc)

        
Safe_Token = Safecoin_Token()
Safe_Token.Run()


