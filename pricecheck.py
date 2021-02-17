import requests
import json
import time
import telegram

token="1669932102:AAHV28DSzEZbUQos-1h0lgPO4yrziGBiAIk"
bot=telegram.Bot(token=token)
url = "https://api.binance.com/api/v3/ticker/price?symbol={}BUSD"
TRX = 1
ADA = 1
LINK = 1
XLM = 1
BNB = 1

while True :
    response = requests.get(url.format('TRX'))
    Json = response.json()
    now_TRX = float(Json['price'])

    response = requests.get(url.format('ADA'))
    Json = response.json()
    now_ADA = float(Json['price'])

    response = requests.get(url.format('LINK'))
    Json = response.json()
    now_LINK = float(Json['price'])

    response = requests.get(url.format('XLM'))
    Json = response.json()
    now_XLM = float(Json['price'])

    response = requests.get(url.format('BNB'))
    Json = response.json()
    now_BNB = float(Json['price'])

    TRX_dif = (now_TRX - TRX) / TRX
    ADA_dif = (now_ADA - ADA) / ADA
    LINK_dif = (now_LINK - LINK) / LINK
    XLM_dif = (now_XLM - XLM) / XLM
    BNB_dif = (now_BNB - BNB) / BNB

    diffs = {'TRX':TRX_dif, 'ADA':ADA_dif, 'LINK':LINK_dif, 'XLM':XLM_dif, 'BNB':BNB_dif}
    def f(x):
        return diffs[x]
    key_max = max(diffs.keys(), key=f)
    diff = round(diffs[key_max]*100, 2)
    bot.send_message(chat_id="@defi_alert_milleniz", text="{}가 {}% 만큼 올랐습니다".format(key_max, diff))

    TRX = now_TRX
    ADA = now_ADA
    LINK = now_LINK
    XLM = now_XLM
    BNB = now_BNB
    time.sleep(60)
    

