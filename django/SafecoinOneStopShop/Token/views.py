from django.shortcuts import render

from django.http import HttpResponse,JsonResponse

from SafeConnect import SafeToken
ST = SafeToken()
def index(request):
    #print(request.POST)
    return render(request, "index.html")

def WalletPopup(request):
    pass


    
def Wallet(request):
    print(request.POST.get("keypair", ""))
    keypair = request.POST.get("keypair", "")
    print("keypair wallet: ",keypair)
    Keypair = ST.WalletConnect(keypair)
    print("pubkey: ",Keypair.public_key)
    return HttpResponse(str(Keypair.public_key))


def WalletNew(request):
    keypair = ST.walletNew()
    print('Keypair new : ',keypair.seed)
    print([b for b in keypair.seed])
    return JsonResponse({'seed':str([b for b in keypair.seed]),'pubkey':str(keypair.public_key)})

def NewToken(request):
    TokenPubKey = ST.NewToken()
    return HttpResponse(str(TokenPubKey))


def ChangeChain(request):
    chain = request.POST.get("chain", None)
    #print("Chain: ",chain)
    endpoint = ST.ChangeEndpoint(chain)
    print('endpoint : ',endpoint)
    return JsonResponse({'endpoint':endpoint})
def Balance(request):
    (bal, SafeValue, BWorth) = ST.Balance()
    return JsonResponse({'bal':bal,'SafeValue':SafeValue,'BWorth':BWorth})

def airdrop(request):
    tx = ST.airdrop()
    return HttpResponse(tx)
