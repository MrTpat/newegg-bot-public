import requests
import base64
import json
import sys
import configparser
import colors
import time



def loadCookies() -> dict:
    with open('cookies.json', 'r') as fh:
            newCookies = json.load(fh)
            return newCookies

def addToCart(p_id: str, cookies: dict, isCombo: bool) -> bool:
    try:
        if isCombo:
            add = requests.get('https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList=Combo.' + p_id, cookies=cookies)
        else:
            add = requests.get('https://secure.newegg.com/Shopping/AddtoCart.aspx?Submit=ADD&ItemList=' + p_id, cookies=cookies)
    except:
        colors.printFail("Failed to add to cart, IP block?")
        time.sleep(2)
        return addToCart(p_id, cookies)
    if p_id not in add.url: #fail
        colors.printFail("Couldn't add to cart, retrying in 1 sec")
        time.sleep(2)
        return addToCart(p_id, cookies, isCombo)
    else:
        colors.printInfo("Added to cart")
        return True

def genDataString(p_id: str, s_id: str, isCombo: bool) -> str:
    if not isCombo:
        rawMid = '{"SaleType":1,"ItemGroup":1,"ItemNumber":"' + s_id + '","OptionalInfos":[]}'
        encryptedBytes = base64.standard_b64encode(str.encode(rawMid)).decode()
    else:
        rawMid = '{"SaleType":1,"ItemGroup":3,"ItemNumber":"' + p_id + '","OptionalInfos":[]}'
        encryptedBytes = base64.standard_b64encode(str.encode(rawMid)).decode()
    return '{"ItemList":[{"ItemNumber":"' + s_id + '","ItemKey":"' + encryptedBytes + '","Quantity":1}],"Actions":[]}'

def genSessionID(cookies: dict, p_id: str, s_id: str, isCombo: bool) -> str:
    req_url = 'https://secure.newegg.com/shop/api/CheckoutApi'
    headers = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://secure.newegg.com/shop/cart',
            'accept-language': 'en-US,en;q=0.9'
            }
    data = genDataString(p_id, s_id, isCombo)
    requestObj = requests.post(req_url, headers=headers, cookies=cookies, data=data)
    if requestObj.status_code != 200:
        colors.printFail("ERROR GENERATING SESSION ID, TRYING AGAIN")
        return genSessionID(cookies, p_id, s_id, isCombo)
    else:
        colors.printInfo("GOT SESSION ID")
        return requestObj.json()['SessionID']

def getTransactionNumber(cookies: dict, session_id: str) -> str:
    headers = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-sessionid': session_id,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://secure.newegg.com/shop/checkout?sessionId=' + session_id,
            'accept-language': 'en-US,en;q=0.9'
            }
    data = '{"SessionID":"' + session_id + '","Actions":[{"ActionType":"AlterPanelStatus","JsonContent":"{\\"ActionType\\":\\"AlterPanelStatus\\",\\"PanelStatus\\":{\\"ShippingAddress\\":\\"Done\\",\\"DeliveryMethod\\":\\"Done\\",\\"TaxID\\":\\"Done\\",\\"Payment\\":\\"Todo\\"}}"}],"EnableAsyncToken":true}'
    responseObj = requests.post('https://secure.newegg.com/shop/api/InitOrderReviewApi', headers=headers, cookies=cookies, data=data)
    if responseObj.status_code != 200:
        printFail("ERROR GETTING TRANSACTION NUMBER, TRYING AGAIN")
        return getTransactionNumber(cookies, session_id)
    else:
        colors.printInfo("GOT TRANSACTION NUMBER")
        try:
            return str(responseObj.json()['PaymentOption']['CreditCardList'][0]['TransactionNumber'])
        except:
            colors.printFail("ERROR GETTING TRANSACTION NUMBER, PLEASE RUN THE GENCOOKIE UTILITY!!!")
            return None

def submitCardInfo(transactionNumber: str, cookies: dict, cvv: str, session_id: str, trans_number: str) -> bool:
    headers = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-sessionid': session_id,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://secure.newegg.com/shop/checkout?sessionId=' + session_id,
            'accept-language': 'en-US,en;q=0.9'
            }
    data = '{"SessionID":"' + session_id + '","Actions":[{"ActionType":"ConfirmPayment","JsonContent":"{\\"ActionType\\":\\"ConfirmPayment\\",\\"Cvv2\\":\\"' + cvv + '\\",\\"TransactionNumber\\":' + trans_number + ',\\"PaytermsCode\\":\\"Discover\\"}"}],"EnableAsyncToken":true}'
    responseObj = requests.post('https://secure.newegg.com/shop/api/InitOrderReviewApi', headers=headers, cookies=cookies, data=data)
    if responseObj.status_code != 200:
        colors.printFail("ERROR SUBMITTING CARD INFO, TRYING AGAIN")
        return submitCardInfo(transactionNumber, cookies, cvv, session_id, trans_number)
    else:
        colors.printInfo("CARD INFO SUBMITTED")
        return True

def validateAddress(config: dict, cookies: dict, s_id: str, trans_number: str) -> bool:
    headers = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-sessionid': s_id,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://secure.newegg.com/shop/checkout?sessionId=' + s_id,
            'accept-language': 'en-US,en;q=0.9'
            }

    data = getBillingData(config, trans_number)
    response = requests.post('https://secure.newegg.com/shop/api/ValidateAddress', headers=headers, data=data, cookies=cookies)
    if response.status_code != 200:
        colors.printFail("ERROR VALIDATING BILLING ADDRESS, RETRYING...")
        return validateAddress(config, cookies, s_id)
    else:
        colors.printInfo("BILLING ADDRESS VALIDATED")
        return True

def submit_order(cookies: dict, s_id: str) -> bool:
    headers = {
            'authority': 'secure.newegg.com',
            'accept': 'application/json, text/plain, */*',
            'x-sessionid': s_id,
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.57',
            'content-type': 'application/json',
            'origin': 'https://secure.newegg.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://secure.newegg.com/shop/checkout?sessionId=' + s_id,
            'accept-language': 'en-US,en;q=0.9'
            }

    data = '{"SessionID":"' + s_id + '","IsAcceptNSCCAuth":false,"SubscribeNewsletterFlag":false,"CreactAccount":false,"Password":"","MobileSubscribe":{},"LanguageCode":"en-us","Cvv2":""}'
    response = requests.post('https://secure.newegg.com/shop/api/PlaceOrderApi', headers=headers, data=data, cookies=cookies)
    if response.status_code != 200:
        colors.printFail("FAILED TO PLACE. RETRYING...")
        return submit_order(cookies, s_id)
    else:
        colors.printInfo("ORDER PLACED")
        return True
    

def checkout(config: dict, cookies: dict, p_id: str, s_id: str, cvv: str, test: bool, isCombo: bool) -> bool:
    sessionId = genSessionID(cookies, p_id, s_id, isCombo)
    url = 'https://secure.newegg.com/shop/checkout?sessionId=' + sessionId
    transactionNumber = getTransactionNumber(cookies, sessionId)
    if transactionNumber == None:
        return False
    if submitCardInfo(transactionNumber, cookies, cvv, sessionId, transactionNumber):
        if validateAddress(config, cookies, sessionId, transactionNumber):
            if not test:
                if submit_order(cookies, sessionId):
                    colors.printSuccess("Success! Check your inbox")
                    return True
            else:
                colors.printInfo('session_id: ' + sessionId)
                colors.printInfo('transaction_number: ' + transactionNumber)
                return True
        else:
            return checkout(config, cookies, p_id, s_id, cvv)

    else:
        colors.printFail("Couldnt check out, retrying")
        return checkout(config, cookies, p_id, s_id)
    return True

def testCookies() -> bool:
    cookies = loadCookies()
    config = configparser.ConfigParser()
    config.read('config.ini')
    product_id = config['ALWAYSWORKS']['primaryId']
    secondary_product_id = config['ALWAYSWORKS']['secondaryId']
    cvv = config['CREDENTIALS']['cvv']
    colors.printInfo('Running in always successful mode (no buying)')
    addToCart(product_id, cookies)
    transactionComplete = checkout(config, cookies, product_id, secondary_product_id, cvv, True)
    if not transactionComplete:
        colors.printFail('Need to update cookies!')
    else:
        colors.printSuccess('Cookies working...')
    return transactionComplete

def getBillingData(config: dict, transNumber: str) -> str:
    billData = config['CREDENTIALS']
    name = billData['name']
    phone = billData['phone']
    country = billData['country']
    countryLong = billData['countryLong']
    state = billData['state']
    city = billData['city']
    address = billData['address']
    zipCode = billData['zipCode']
    return f'{{"TransNumber":{transNumber},"AddressLabel":"Untitled","ContactWith":"{name}","Phone":"{phone}","Fax":"","Country":"{country}","State":"{state}","City":"{city}","Address1":"{address}","Address2":"","ZipCode":"{zipCode}","IsDefault":false,"DisplayLines":["{address}","{city}, {state} {zipCode}","{countryLong}","{phone}"],"AddressVerifyMark":"Verified","Email":null,"DisableEmail":false,"CompanyName":"","LanguageCode":null,"IsSelected":false,"SaveAddress":false,"QASDisplayLines":["{address}","{city}, {state} {zipCode}","{countryLong}"]}}'


def main(profile: str) -> None:
    cookies = loadCookies()
    transactionComplete = False
    config = configparser.ConfigParser()
    config.read('config.ini')
    product_id = config[profile]['primaryId']
    secondary_product_id = config[profile]['secondaryId']
    isCombo = config[profile]['isCombo'] == 'true'
    cvv = config['CREDENTIALS']['cvv']
    test = False
    if profile == 'TEST' or 'COMBOTEST':
        colors.printInfo('Running in test mode (no buying)')
        test = True
    
    while not transactionComplete:
        if addToCart(product_id, cookies, isCombo):
            transactionComplete = checkout(config, cookies, product_id, secondary_product_id, cvv, test, isCombo)


if __name__ == "__main__":
        if len(sys.argv) != 1:
            colors.printFail('CONFIRM YOU WANT TO RUN THE ACTUAL SCRIPT FOR PROFILE: ' + sys.argv[1])
            input()
            main(sys.argv[1])
        else:
            main('TEST')

