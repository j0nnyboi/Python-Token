from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi  
from io import BytesIO
import json
import io
import json                    
import base64                  
import logging             
import numpy as np
from PIL import Image
from urllib.parse import urlparse, parse_qs
import gzip
import zlib
import subprocess
import os
import requests
import ssl
import argparse
import string
import random
import json
import time
import base58
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.publickey import PublicKey
from arweave.arweave_lib import Wallet, Transaction
from arweave.transaction_uploader import get_uploader
from arweave_testnet.arweave_lib import Wallet as Wallet_testnet
from arweave_testnet.arweave_lib import Transaction as Transaction_testnet
from arweave_testnet.transaction_uploader import get_uploader as get_uploader_testnet
from socketserver import ThreadingMixIn
import threading
import urllib



hostName = "localhost"
serverPort = 8088


def checkSafeTransation(transactionIP,env):
    try:
        if(env == 'mainnet-beta'):
            api_endpoint = "https://api.mainnet-beta.safecoin.org"
        elif('devnet' in env):
            api_endpoint = "https://api.devnet.safecoin.org"
        elif(env == 'testnet'):
            api_endpoint = "https://api.testnet.safecoin.org"
            
        client = Client(api_endpoint)
        rec = client.get_confirmed_transaction(transactionIP)
        #print(rec)
        keys = rec['result']['transaction']['message']['accountKeys']
        for k in keys:
            if"es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc" in k:
                return True
        time.sleep(0.5)
        rec = client.get_confirmed_transaction(transactionIP)
        keys = rec['result']['transaction']['message']['accountKeys']
        for k in keys:
            if"es7DKe3NyR1u8MJNuv6QV6rbhmZQkyYUpgKpGJNuTTc" in k:
                return True
        return False
    except:
        return False
    

class HTTPRequestHandler(BaseHTTPRequestHandler):
        
    def do_GET(self):
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'{"Hello":"You"}')
        print("someone trying to get data")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) 
        post_data = self.rfile.read(content_length)
        print(post_data)


        transaction = post_data["transaction"]
        print('transaction : ', transaction)
        env = post_data["env"]
        print('network : ',env)
        Error = checkSafeTransation(transaction,env)
        print("Trans Found : ",Error)
        if(Error == True):
            if(env == 'testnet' or env == 'devnet'):
                wallet = Wallet_testnet('C:\\Users\\Administrator\\Desktop\\ArweaveBridge-main\\arweave-keyfile_testnet.json')
                get_uploader_AR = get_uploader_testnet
                Transaction_AR = Transaction_testnet
                ARreturnLink = "https://safestore.ledamint.io/"
            elif(env == 'mainnet' or env == 'mainnet-beta'):
                wallet = Wallet('C:\\Users\\Administrator\\Desktop\\ArweaveBridge-main\\arweave-keyfile.json')
                get_uploader_AR = get_uploader
                Transaction_AR = Transaction
                ARreturnLink = "https://arweave.net/"
            else:
                returnMessage = {}
                returnMessage["status"] = "Failed"
                returnMessage["transactionId"] = "EEOR"
                returnMessage["error"] = "Chain ERROR"
                responsjson["error"] = "Chain ERROR"
                EncodedReturnJson = json.dumps(returnMessage).encode()
                print('AreweaveJson ' ,EncodedReturnJson)
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(EncodedReturnJson)




            




class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


#httpd = HTTPServer(('127.0.0.1', 5050), HTTPRequestHandler)
httpd = ThreadingSimpleServer(('127.0.0.1', 5050), HTTPRequestHandler)
httpd.serve_forever()




        
