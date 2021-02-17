from selenium import webdriver
from explicit import waiter, XPATH
from bs4 import BeautifulSoup
import time
import requests
import telegram

token="1669932102:AAHV28DSzEZbUQos-1h0lgPO4yrziGBiAIk"
bot=telegram.Bot(token=token)
driver_path = "C:/Users/wndrms/Desktop/selenium/chromedriver"
url = "https://exchange.linear.finance/?token=l{}"
url2 = "https://api.binance.com/api/v3/ticker/price?symbol={}BUSD"

while True:
    price_linear = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0}
    price_binance = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0}
    diffs = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0}

    driver = webdriver.Chrome(driver_path)
    for token in price_linear:
        driver.get(url.format(token))
        time.sleep(3)
        price = waiter.find_element(driver, "/html/body/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[1]", by=XPATH)
        price_linear[token] = float(price.text.replace('$', ''))
    driver.quit()

    for token in price_binance:
        response = requests.get(url2.format('TRX'))
        Json = response.json()
        price_binance[token] = float(Json['price'])

    for token in diffs:
        diffs[token] = (price_binance[token] - price_linear[token]) / price_linear[token]
    def f(x):
        return diffs[x]
    key_max = max(diffs.keys(), key=f)
    diff = round(diffs[key_max]*100, 2)
    bot.send_message(chat_id="@defi_alert_milleniz", text="{}가 {}% 만큼 올랐습니다".format(key_max, diff))
    time.sleep(60)
    