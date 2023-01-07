from django.shortcuts import render

from django.http import HttpResponse

from SafeConnect import SafeToken
ST = SafeToken()
def index(request):
    #print(request.POST)
    return render(request, "Home.html")

def Wallet(request):
    print(request.POST.get("keypair", ""))
    keypair = request.POST.get("keypair", "")
    print("keypair: ",keypair)
    Keypair = ST.WalletConnect(keypair)
    print("pubkey: ",Keypair.public_key)
    return HttpResponse(str(Keypair.public_key))

def WalletNew(request):
    keypair = ST.walletNew()
    print('Keypair : ',keypair.seed)
    print([b for b in keypair.seed])
    return HttpResponse(str([b for b in keypair.seed]))
