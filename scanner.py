import requests
import buyBot
import sys
import colors
import configparser
import time
from notify import notify


def inStock(s_id: str, price: float) -> bool:
    url = 'https://www.newegg.com/product/api/ProductRealtime?ItemNumber=' + s_id
    try:
        r = requests.get(url)
    except:
        colors.printFail('Failed to make request to instock API, trying again...')
        return inStock(s_id, price)
    if r.status_code == 200:
        try:
            j = r.json()
            inStock = j['MainItem']['Instock']
            acceptPrice = j['MainItem']['FinalPrice'] <= price
            if inStock and acceptPrice:
                colors.printSuccess('ITEM IN STOCK FOR GOOD PRICE!!!')
            elif inStock and not acceptPrice:
                colors.printFail('Item in stock, price too high...')
            else:
                colors.printInfo('Item not in stock...')
            return inStock and acceptPrice
        except:
            colors.printFail('Invalid response, IP block?')
            return False
    else:
        colors.printFail('Unsuccessful request made, IP block?')
        return False


profile = ''
if len(sys.argv) == 1:
    profile = 'TEST'
    colors.printInfo('Running in test mode...')
else:
    profile = sys.argv[1]
    colors.printFail('CONFIRM YOU WANT TO RUN THE ACTUAL SCRIPT FOR CONFIG: ' + profile)
    input()
config = configparser.ConfigParser()
config.read('config.ini')
secondary_product_id = config[profile]['secondaryId']
price = float(config[profile]['priceThreshold'])
phoneNumber = config['CREDENTIALS']['phoneNumber']
email = config['CREDENTIALS']['email']
emailPassword = config['CREDENTIALS']['emailPassword']
server = config['CREDENTIALS']['server']
bought = False
iterationsUntilCookieTest = 90
iterations = 0
while not bought:
   if iterations == iterationsUntilCookieTest:
       notify("Need to refresh cookies!", email, emailPassword, server, phoneNumber)
       colors.printFail("Need to refresh cookies!")
       iterations = 0
   if inStock(secondary_product_id, price):
       buyBot.main(profile)
       bought = True
       notify("Bought item. Check newegg.", email, emailPassword, server, phoneNumber)
   else:
       iterations = iterations + 1
       time.sleep(30)
