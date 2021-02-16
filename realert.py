import telegram
import requests
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
import time

token="1669932102:AAHV28DSzEZbUQos-1h0lgPO4yrziGBiAIk"
bot=telegram.Bot(token=token)
urllina = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x762539b45a1dcce3d36d080f74d1aed37844b878&address=0xeb325a8ea1c5abf40c7ceaf645596c1f943d0948&tag=latest&apikey=MYC6KM6E7AH8CV6GU8TH278M5GVUF1GNWR"
urlbusd = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&address=0xeb325a8ea1c5abf40c7ceaf645596c1f943d0948&tag=latest&apikey=MYC6KM6E7AH8CV6GU8TH278M5GVUF1GNWR"

cmc = CoinMarketCapAPI('c1d0800c-8429-48a1-b943-e5d37fa42ebb')

while True:
    response1 = requests.get(urllina)
    Json1 = response1.json()

    response1 = requests.get(urlbusd)
    Json2 = response1.json()

    lina = int(Json1['result'])
    busd = int(Json2['result'])
    pool_price = round(busd/lina, 5)

    r = cmc.cryptocurrency_info(symbol='lina')
    description = r.data['LINA']['description']
    strings = description.split(" ")
    price = float(strings[strings.index('USD') - 1])
    price = round(price, 5)

    dif = price / pool_price * 100 - 100
    dif = round(dif, 2)
    bot.send_message(chat_id="@defi_alert_milleniz", text="pool price : {}\ncoin price(CoinMarketCap) : {}\n 차이 : {}%".format(pool_price, price, dif))
    time.sleep(300)

