from selenium import webdriver
from explicit import waiter, XPATH
from bs4 import BeautifulSoup
import time
import requests
import telegram

token="1669932102:AAHV28DSzEZbUQos-1h0lgPO4yrziGBiAIk"
bot=telegram.Bot(token=token)
driver_path = '/usr/bin/chromedriver'
url = "https://exchange.linear.finance/?token=l{}"
url2 = "https://api.binance.com/api/v3/ticker/price?symbol={}BUSD"

while True:
    price_linear = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0, 'YFI':0, 'DOT':0}
    price_binance = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0, 'YFI':0, 'DOT':0}
    diffs = {'TRX':0, 'ADA':0, 'LINK':0, 'XLM':0, 'BNB':0, 'YFI':0, 'DOT':0}
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
    driver = webdriver.Chrome(driver_path, options=options)
    for token in price_linear:
        driver.get(url.format(token))
        time.sleep(3)
        price = waiter.find_element(driver, "/html/body/div[1]/div/div/div/div/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div[1]", by=XPATH)
        price_linear[token] = float(price.text.replace('$', '').replace(',', ''))
    driver.quit()

    for token in price_binance:
        response = requests.get(url2.format(token))
        Json = response.json()
        price_binance[token] = float(Json['price'])

    for token in diffs:
        diffs[token] = (price_binance[token] - price_linear[token]) / price_linear[token]
    '''    
    def f(x):
        return diffs[x]
    key_max = max(diffs.keys(), key=f)
    diff = round(diffs[key_max]*100, 2)
    '''
    text=""
    for token in diffs:
        dif = round(diffs[token]*100, 2)
        text = text + "\n{} : {}$ | {}$ | {}%갭 ".format(token, price_binance[token], price_linear[token], dif)
        if dif >= 1.0:
            text = text + "🚀🚀🚀"
    bot.send_message(chat_id="@defi_alert_milleniz", text=text)
    time.sleep(60)
    
