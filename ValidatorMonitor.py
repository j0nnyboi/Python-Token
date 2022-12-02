
import requests
from discord import Webhook, RequestsWebhookAdapter
from time import gmtime, strftime,sleep

from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.rpc.types import MemcmpOpts
from safecoin.publickey import PublicKey


ValidatorCheckTime = 5 #time in minutes between checking for you validator is off line
Minpre = 0
Daypre = 0
hourpre = 0
Counter = 99
AlarmSent = False

def DiscordSend(StringToSend):
        webhook.send(StringToSend)

def ValidatorMonitor(api_endpoint,client,ValidatorID,ValidatorVote,VoteBalanceWarn,IdentityBalanceWarn,webhook,Min):
    

    hour = strftime("%H", gmtime())
    if(hour != hourpre):
            hourpre = hour
            AlarmSent = False
            day = strftime("%d", gmtime())
            if(day != Daypre):
                Daypre = day
                if(client.is_connected()): 
                    VoteBalance = int(client.get_balance(ValidatorVote)['result']['value'])/1000000000
                    print("Vote account balance = ",VoteBalance)
                    if(VoteBalance > VoteBalanceWarn):
                        DiscordSend("you have earnt to much safe, to be on your validator, time to move it,amount is %s use (~/Safecoin/target/release/safecoin withdraw-from-vote-account VoteAddress DesternationWallet amount)"% VoteBalance)
                    IDBalance = int(client.get_balance(ValidatorID)['result']['value'])/1000000000
                    print("Identity account balance = ",IDBalance)
                    if(IDBalance < IdentityBalanceWarn):
                        DiscordSend("Running out of safe, you only have %s left to vote with, please add some to address %s" % (IDBalance,ValidatorID))
                else:
                    client = Client(api_endpoint)
            

        Counter += 1
        if(Counter >= ValidatorCheckTime):
                Counter = 0
                if(client.is_connected() == True):
                    validatorList = (client.get_vote_accounts()['result']['delinquent'])
                    print("Latest delinquent validators")
                    for vals in validatorList:
                        nodePubkey = vals['nodePubkey']
                        votePubkey = vals['votePubkey']
                        print(nodePubkey,votePubkey)
                        if(ValidatorID in nodePubkey or ValidatorID in votePubkey):
                            print("^^^^^^^^^^^^^^^^^^^found my Validator^^^^^^^^^^^^^^^^^^")
                            if(AlarmSent == False):
                                DiscordSend("Your validator has gone off line")
                                AlarmSent = True
                    print("")
                else:
                    client = Client(api_endpoint)                        
                        
                        
                        

