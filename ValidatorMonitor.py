
import requests

from time import gmtime, strftime,sleep
from discord import Webhook, RequestsWebhookAdapter
from safecoin.keypair import Keypair
from safecoin.rpc.api import Client
from safecoin.rpc.types import MemcmpOpts
from safecoin.publickey import PublicKey

class ValidatorMonitor(object):
        def __init__(self,Discord_Web_Hock,ValidatorIDs):
                self.ValidatorCheckTime = 5 #time in minutes between checking for you validator is off line
                self.Daypre = 0
                self.hourpre = 0
                self.Counter = 99
                self.MYcommission = {}
                self.AlarmSent = False
                for ids in ValidatorIDs:
                        self.MYcommission[ids] = 101
                self.MYcommissionPre = {}
                self.webhook = Webhook.from_url(Discord_Web_Hock, adapter=RequestsWebhookAdapter())

        def DiscordSend(self,StringToSend):
                self.webhook.send(StringToSend)

        def MYMonitor(self,api_endpoint,client,ValidatorID,ValidatorVote,VoteBalanceWarn,IdentityBalanceWarn):
            

                hour = strftime("%H", gmtime())
                if(hour != self.hourpre):
                    self.hourpre = hour
                    AlarmSent = False
                    day = strftime("%d", gmtime())
                    if(day != self.Daypre):
                        self.Daypre = day
                        if(client.is_connected()): 
                            VoteBalance = int(client.get_balance(ValidatorVote)['result']['value'])/1000000000
                            print("Vote account balance = ",VoteBalance)
                            print(ValidatorID)
                            if(VoteBalance > VoteBalanceWarn):
                                self.DiscordSend("you have earnt to much safe, to be on your validator, time to move it,amount is %s use (~/Safecoin/target/release/safecoin withdraw-from-vote-account VoteAddress DesternationWallet amount)"% VoteBalance)
                            IDBalance = int(client.get_balance(ValidatorID)['result']['value'])/1000000000
                            print("Identity account balance = ",IDBalance)
                            if(IDBalance < IdentityBalanceWarn):
                                self.DiscordSend("Running out of safe, you only have %s left to vote with, please add some to address %s" % (IDBalance,ValidatorID))
                        else:
                            client = Client(api_endpoint)
                    

                self.Counter += 1
                if(self.Counter >= self.ValidatorCheckTime):
                        self.Counter = 0
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
                                        self.DiscordSend("Your validator has gone off line")
                                        self.AlarmSent = True
                            print("")
                        else:
                            client = Client(api_endpoint)                        
                                

        def OtherMonitor(self,api_endpoint,client,ValidatorIDs):                    
                    

                self.Counter += 1
                if(self.Counter >= self.ValidatorCheckTime):
                        self.Counter = 0
                        if(client.is_connected() == True):
                                validatorList = (client.get_vote_accounts()['result'])
                                current = validatorList['current']
                                deliquennt = validatorList['delinquent']
                            
                                print("Latest delinquent validators")
                                for ValidatorID in ValidatorIDs:
                                        for vals in deliquennt:
                                                nodePubkey = vals['nodePubkey']
                                                votePubkey = vals['votePubkey']
                                                commission = vals['commission']
                                                print(nodePubkey,votePubkey)
                                                
                                                if(ValidatorID in nodePubkey or ValidatorID in votePubkey):
                                                    print("^^^^^^^^^^^^^^^^^^^found Validator^^^^^^^^^^^^^^^^^^")
                                                    if(AlarmSent == False):
                                                        self.DiscordSend("validator has gone off line")
                                                        self.AlarmSent = True
                                                
                                print("Latest running validators")
                                for ValidatorID in ValidatorIDs:
                                        for vals in current:
                                                nodePubkey = vals['nodePubkey']
                                                votePubkey = vals['votePubkey']
                                                commission = vals['commission']
                                                print(nodePubkey,votePubkey)
                                                
                                                if(ValidatorID in nodePubkey or ValidatorID in votePubkey):
                                                    print("^^^^^^^^^^^^^^^^^^^found Validator^^^^^^^^^^^^^^^^^^")
                                                    if(MYcommission == 101):
                                                            self.MYcommissionPre[ValidatorID] = commission#getting right commision first time
                                                    MYcommission = commission
                                                    if(MYcommission != self.MYcommissionPre[ValidatorID]):
                                                            print("Commision has changed")
                                                            self.DiscordSend("Commision has changed on valitador from %s%% to %s%%" %(ValidatorID,MYcommissionPre,MYcommission))
                                                            self.MYcommissionPre[ValidatorID] = MYcommission
                        
                        
                            
                        else:
                            client = Client(api_endpoint)
                        
class validatorInfo(object):
        def __init__(self,client):
                self.client = client

        def getVal(self):
                #print(client.get_vote_accounts())
                returnLst ={}
                validatorList = (self.client.get_vote_accounts()['result'])
                current = validatorList['current']
                for lst in current:
                        #print(lst['votePubkey'])
                        #print(lst['activatedStake'])
                        #print(lst['commission'])
                        #print(self.get_stake_activation(lst['votePubkey']),lst['votePubkey'])
                        returnLst[lst['votePubkey']] = {}
                        returnLst[lst['votePubkey']]['Com'] = lst['commission']
                        returnLst[lst['votePubkey']]['stake'] = lst['activatedStake']
                        #TokenText.insert(tkinter.END,"Validator: %s Commision: %d stake: %s \n"% (lst['votePubkey'],lst['commission'],lst['activatedStake']))
                #deliquennt = validatorList['delinquent']
                return returnLst

        def get_stake_activation(self, pubkey):
                return self.client.get_stake_activation(pubkey)
