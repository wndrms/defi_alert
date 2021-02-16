import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
import requests
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError

token="1669932102:AAHV28DSzEZbUQos-1h0lgPO4yrziGBiAIk"
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
urllina = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0x762539b45a1dcce3d36d080f74d1aed37844b878&address=0xeb325a8ea1c5abf40c7ceaf645596c1f943d0948&tag=latest&apikey=MYC6KM6E7AH8CV6GU8TH278M5GVUF1GNWR"
urlbusd = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress=0xe9e7cea3dedca5984780bafc599bd69add087d56&address=0xeb325a8ea1c5abf40c7ceaf645596c1f943d0948&tag=latest&apikey=MYC6KM6E7AH8CV6GU8TH278M5GVUF1GNWR"
urllp = "https://api.bscscan.com/api?module=stats&action=tokensupply&contractaddress=0xeb325a8ea1c5abf40c7ceaf645596c1f943d0948&apikey=MYC6KM6E7AH8CV6GU8TH278M5GVUF1GNWR"
cmc = CoinMarketCapAPI('c1d0800c-8429-48a1-b943-e5d37fa42ebb')

def call_account():
    f = open('account.txt', 'r')
    account = f.readline()
    account = account.split(' ')
    return account[0], account[1], account[2]

def update(update, context):
    if (len(context.args) == 3) :
        f = open('account.txt', 'w')
        f.write("{} {} {}".format(context.args[0], context.args[1], context.args[2]))
        context.bot.send_message(chat_id=update.effective_chat.id, text="LINA, BUSD, LP 수량이 업데이트 되었습니다")
    else :
        context.bot.send_message(chat_id=update.effective_chat.id, text="입력이 잘못되었습니다. 다시 입력해주세요")

def now(update, context):
    (firstlina, firstbusd, firstlp) = call_account()
    response = requests.get(urllp)
    Json = response.json()
    lp_total = int(Json['result'])
    firstlina = int(firstlina)
    firstbusd = int(firstbusd)
    firstlp = int(firstlp)

    response1 = requests.get(urllina)
    Json1 = response1.json()

    response1 = requests.get(urlbusd)
    Json2 = response1.json()

    lina_total = int(Json1['result'])
    busd_total = int(Json2['result'])
    
    lina_now = lina_total * (firstlp / lp_total)
    busd_now = busd_total * (firstlp / lp_total)

    r = cmc.cryptocurrency_info(symbol='lina')
    description = r.data['LINA']['description']
    strings = description.split(" ")
    price = float(strings[strings.index('USD') - 1])

    value = lina_now * price + busd_now
    value = round(value, 2)
    value_first = firstlina * price + firstbusd
    value_first = round(value_first, 2)
    context.bot.send_message(chat_id=update.effective_chat.id, text="현재 자산 가치는 {}$ 입니다\n 원래 자산가치는 {}$ 입니다".format(value, value_first))

    

update_handler = CommandHandler('update', update)
now_handler = CommandHandler('now', now)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(now_handler)

updater.start_polling()
updater.idle()