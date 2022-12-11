from pycoingecko import CoinGeckoAPI


CoinGeko = CoinGeckoAPI()
        
def getLatestPrice(safeAmount):
    safePrice = CoinGeko.get_price(ids='safe-coin-2', vs_currencies='usd')['safe-coin-2']['usd']
    #print(safePrice * safeAmount)
    return (safePrice, safePrice * safeAmount)

def getLatestPriceArweave():
    arweavePrice = CoinGeko.get_price(ids='arweave', vs_currencies='usd')['arweave']['usd']
    return (arweavePrice)


